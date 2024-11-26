import logging
from typing import Dict


class Logger:
    """Logger setup for the application."""

    def __init__(self, log_file: str) -> None:
        """Initialize the logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # File handler for logging
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


class ProcessFlowLog:
    """Class to process flow logs and compute port/protocol and tag counts."""

    def __init__(self, flow_log_file: str, tag_map_file: str, logger: logging.Logger) -> None:
        """
        Initialize the ProcessFlowLog class.

        Args:
            flow_log_file: Path to the flow log file.
            tag_map_file: Path to the tag map file.
            logger: Configured logger instance.
        """
        self.flow_log_file = flow_log_file
        self.tag_map_file = tag_map_file
        self.port_protocol_count_file = "./process_flowlog_op_file.txt"
        self.port_protocol_counts: Dict[str, int] = {}
        self.tag_counts: Dict[str, int] = {}
        self.tag_map: Dict[str, str] = {}
        self.logger = logger

        # Load the tag lookup table into memory
        self._load_tag_map()

    def _load_tag_map(self) -> None:
        """Load the tag lookup table into memory."""
        try:
            with open(self.tag_map_file, "r") as rfile:
                for line in rfile:
                    l_split = line.strip().split(",")
                    self.tag_map["_".join(l_split[:2])] = l_split[-1]
        except FileNotFoundError as e:
            self.logger.error(f"Tag map file not found: {e}")
            raise

    def process_flowlog(self) -> None:
        """
            This method processes the flow log and updates port/protocol and tag counts.
            It also assumes that each flowlog has atleast 8 fields or more as
            it has to parse out the dstport and protocol from each line i.e. index 6 and 7
            of each line.
        """
        try:
            with open(self.flow_log_file, "r") as r_file:
                for line in r_file:
                    fields = line.strip().split(" ")
                    if len(fields) < 8:
                        self.logger.warning(f"Invalid log line: {line.strip()}")
                        continue

                    port_protocol = ",".join(fields[6:8])
                    self.port_protocol_counts[port_protocol] = self.port_protocol_counts.get(port_protocol, 0) + 1

                    if port_protocol in self.tag_map:
                        tag = self.tag_map[port_protocol]
                        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
                    else:
                        self.logger.warning(
                            f"{port_protocol} combination does not have a corresponding tag in the lookup table."
                        )

            self._serialize_op()
        except FileNotFoundError as e:
            self.logger.error(f"Flow log file not found: {e}")
            raise

    def _serialize_op(self) -> None:
        """Write the processed counts to the output file."""
        try:
            with open(self.port_protocol_count_file, "w") as file:
                # Write tag counts
                file.write("Tag Counts:\nTag,Count\n")
                for tag, count in self.tag_counts.items():
                    file.write(f"{tag},{count}\n")
                file.write("\n")

                # Write port/protocol counts
                file.write("Port/Protocol Combination Counts:\nPort,Protocol,Count\n")
                for port_protocol, count in self.port_protocol_counts.items():
                    file.write(f"{port_protocol},{count}\n")
        except IOError as e:
            self.logger.error(f"Error writing to output file: {e}")
            raise


if __name__ == "__main__":
    # Initialize logger
    logger = Logger("process_flowlog.log").get_logger()

    # Create and process the flow log object
    try:
        pfl_object = ProcessFlowLog("./flowlog.txt", "./lookup_table.csv", logger)
        pfl_object.process_flowlog()
    except Exception as e:
        logger.critical(f"An error occurred: {e}")
