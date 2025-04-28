import os
import pandas as pd
import numpy as np

def process_file(path):
    df = pd.read_csv(path)

    # Convert timestamp
    df['frame.time_epoch'] = pd.to_datetime(
        df['frame.time_epoch'],
        errors='coerce',
        format='mixed'
    )

    # Unified ports
    df['src_port'] = df['tcp.srcport'].replace(0, np.nan).fillna(df['udp.srcport'])
    df['dst_port'] = df['tcp.dstport'].replace(0, np.nan).fillna(df['udp.dstport'])

    # Flow ID
    df['flow_id'] = (
        df['ip.src'].astype(str) + "-" +
        df['ip.dst'].astype(str) + "-" +
        df['ip.proto'].astype(str) + "-" +
        df['src_port'].astype(str) + "-" +
        df['dst_port'].astype(str)
    ).apply(hash).astype('int64')

    # Aggregation
    agg_df = df.groupby('flow_id').agg(
        ip_src=('ip.src', 'first'),
        ip_dst=('ip.dst', 'first'),
        proto=('ip.proto', 'first'),
        src_port=('src_port', 'first'),
        dst_port=('dst_port', 'first'),
        packet_count=('frame.len', 'count'),
        total_bytes=('frame.len', 'sum'),
        avg_packet_size=('frame.len', 'mean'),
        std_packet_size=('frame.len', 'std'),
        flow_start=('frame.time_epoch', 'min'),
        flow_end=('frame.time_epoch', 'max'),
        is_malicious=('is_malicious', 'max'),
        tcp_flag_count=('tcp.flags', lambda x: x.notna().sum()),
        small_packets=('frame.len', lambda x: (x < 128).sum())
    ).reset_index()

    # Derived features
    agg_df['flow_start'] = pd.to_datetime(agg_df['flow_start'], errors='coerce')
    agg_df['flow_end'] = pd.to_datetime(agg_df['flow_end'], errors='coerce')
    agg_df['flow_duration'] = (agg_df['flow_end'] - agg_df['flow_start']).dt.total_seconds().replace(0, 1e-6)
    agg_df['bytes_per_second'] = agg_df['total_bytes'] / agg_df['flow_duration']
    agg_df['packets_per_second'] = agg_df['packet_count'] / agg_df['flow_duration']

    # Cleanup
    agg_df['std_packet_size'] = agg_df['std_packet_size'].fillna(-1)
    agg_df.drop(columns=['flow_start', 'flow_end'], inplace=True)

    # Round
    round_cols = ['avg_packet_size', 'std_packet_size', 'flow_duration', 'bytes_per_second', 'packets_per_second']
    agg_df[round_cols] = agg_df[round_cols].round(6)

    # Order columns
    column_order = [
        'flow_id', 'ip_src', 'ip_dst', 'proto', 'src_port', 'dst_port',
        'packet_count', 'total_bytes', 'avg_packet_size', 'std_packet_size', 'small_packets',
        'flow_duration', 'bytes_per_second', 'packets_per_second', 'tcp_flag_count', 'is_malicious'
    ]
    agg_df = agg_df[column_order]

    # Save
    agg_df.to_csv(path, index=False)
    print(f"Processed: {os.path.basename(path)}")

# Batch run on all 17 CSVs
base_path = r"C:\Users\Skeletron\Desktop\dataset"
for i in range(1, 18):
    file_path = os.path.join(base_path, f"{i}.csv")
    process_file(file_path)
