import pandas as pd

# Create a sample dataset
data = {
    'Port': [80, 443, 22, 3306, 21, 8080, 53],
    'Service': ['HTTP', 'HTTPS', 'SSH', 'MySQL', 'FTP', 'HTTP', 'DNS'],
    'Vulnerability': ['SQL Injection', 'SSL/TLS Vulnerability', 'SSH Brute-force', 
                      'SQL Injection', 'Anonymous Login', 'Command Injection', 'DNS Cache Poisoning']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save the dataset to CSV
df.to_csv('vulnerability_dataset.csv', index=False)

print("Dataset created and saved as 'vulnerability_dataset.csv'")

