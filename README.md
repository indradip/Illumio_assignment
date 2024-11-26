Process Flow Log

This program processes network flow logs to count occurrences of specific port/protocol combinations and maps them to corresponding tags using a lookup table. The results are written to an output file, and logs are maintained for any issues encountered during processing.
Assumptions

    Input File Structure:
        The flow log file (flowlog.txt) contains space-separated lines where the 7th and 8th columns represent the dstport and protocol, respectively.
        Example line from flowlog.txt:
        2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK


The tag map file (lookup_table.csv) is a CSV file with entries mapping port and protocol combinations to a tag.
Example line from lookup_table.csv:

        80,tcp,web_traffic

    Output File:
        The results will be written to process_flowlog_op_file.txt in the current directory.
        Output includes:
            Tag Counts: Aggregated counts for tags.
            Port/Protocol Combination Counts: Aggregated counts for each port/protocol combination.

    Error Handling:
        Any invalid or missing lines in the flow log file are logged as warnings.
        If a port/protocol combination from the flow log is not found in the lookup table, a warning is logged.

    Execution Requirements:
        Python 3.6 or later is required.
        Both the flowlog.txt and lookup_table.csv files must exist in the directory where the script is executed.

Program Flow

    The program loads the tag mapping file into memory during initialization.
    It reads each line of the flow log, extracts port/protocol information, and:
        Increments counts for port/protocol combinations.
        Maps the combination to a tag (if available) and increments its count.
    Results are written to an output file, and any errors are logged to my_log.log.

Files
Input Files

    flowlog.txt: The network flow log file containing space-separated entries.
    lookup_table.csv: A CSV file mapping port/protocol combinations to tags.

Output Files

    process_flowlog_op_file.txt: Contains the following sections:
        Tag Counts: Aggregated counts of tags.
        Port/Protocol Combination Counts: Aggregated counts for each port/protocol combination.
    my_log.log: Log file capturing warnings and errors encountered during execution.

Execution
Prerequisites

    Ensure Python 3.6 or later is installed.
    Place the input files (flowlog.txt and lookup_table.csv) in the same directory as the script.

Run the Program

Execute the script using the following command:

python process_flow_log.py

Output Example
process_flowlog_op_file.txt

Tag Counts:
Tag,Count
web_traffic,5
db_traffic,3

Port/Protocol Combination Counts:
Port,Protocol,Count
80,tcp,5
3306,tcp,3

Logging

Warnings and errors are logged to process_flowlog.log:

    Missing lines or invalid formats in the flow log.
    Port/protocol combinations not found in the tag lookup table.

Notable Observation: I think although the lookup table specificall states the first field is the dstport of the flowlog, but the fields themselves that are in the example lookup table file appear to be srcport. I think that's the 
reason we are getting the tag count of the o/p as empty. But I did not change the requirement of the problem as it was stated as such. 