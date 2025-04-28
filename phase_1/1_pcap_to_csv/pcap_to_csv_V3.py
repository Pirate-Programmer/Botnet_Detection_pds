import subprocess

pcap_folder = r"C:\Users\Skeletron\Desktop\temp"
output_folder = r"C:\Users\Skeletron\Desktop\dataset"

fields = [
    "frame.number", "frame.time_epoch", "frame.len",
    "ip.src", "ip.dst", "ip.proto",
    "tcp.srcport", "tcp.dstport", "tcp.flags", "tcp.window_size",
    "udp.srcport", "udp.dstport", "udp.length",
    "dns.qry.name", "http.host"
]
fields_arg = " ".join([f"-e {field}" for field in fields])


for i in range(1, 18):  # Loop from 1 to 17
    pcap_file = f"{pcap_folder}\\{i}.pcap"
    csv_file = f"{output_folder}\\{i}.csv"
    
    tshark_cmd = f'tshark -r "{pcap_file}" -T fields {fields_arg} -E header=y -E separator=, -E quote=d > "{csv_file}"'
    subprocess.run(tshark_cmd, shell=True, check=True)
    
    print(f" Converted: {pcap_file} -> {csv_file}")

print("All files converted!")
