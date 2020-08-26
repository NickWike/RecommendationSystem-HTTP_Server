import re
import time


with open("../logs/RS_Http_Server", "r") as f:
    log_lines = f.readlines()
    for line in log_lines:
        str_time = re.search(r"\d{4}-\d\d-\d\d \d\d", line).group(0)
        t = time.strptime(str_time, "%Y-%m-%d %H")
        file_name = time.strftime("%Y-%m-%d_%H:%M:%S", t) + ".log"
        with open("./logTest/{filename}".format(filename=file_name), "a+") as fin:
            fin.write(line)
        time.sleep(0.5)