import os
import subprocess
import time

SSH_KEY = r"C:\Users\gstore1\.ssh\do_thesis_key"
SERVER_IP = "165.232.65.175"

def run_remote_kubectl(command):
    full_cmd = f'ssh -o StrictHostKeyChecking=no -i "{SSH_KEY}" root@{SERVER_IP} "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml && {command}"'
    subprocess.run(full_cmd, shell=True)

def print_header(title):
    print("\n" + "="*50)
    print(f" {title} ".center(50, "="))
    print("="*50 + "\n")

while True:
    print_header("Zero Trust Security Engine Simulator")
    print("Current Trust Score Algorithm inputs:")
    print("  I (Identity) = Valid SVID (40 pts)")
    print("  H (Health) = Baseline Nominal (40 pts)")
    print("  B (Behavior) = Normal (20 pts)")
    print("\nSelect an action:")
    print("1) Set Status to Normal (Trust Score: 100/100) -> Removes Security Blocks")
    print("2) Simulate Anomaly / Compromise (Trust Score: 60/100) -> Triggers Istio Micro-Segmentation")
    print("3) Exit")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == '1':
        print("\n[+] Calculating Trust Score: 100/100")
        print("[+] Access level is SAFE.")
        print("[+] Policy Engine updating Istio configurations: REMOVING BLOCKS...")
        run_remote_kubectl("kubectl delete authorizationpolicy dynamic-trust-isolation -n banking --ignore-not-found")
        print("\n=> Try loading the banking app in your browser! It should work normally.")
        time.sleep(2)
        
    elif choice == '2':
        print("\n[!] ALERT: Unexpected system call detected in application container.")
        print("[-] Trust Score Behavior penalty: -40 pts")
        print("[!] New Trust Score calculated: 60/100 (Below required threshold of 90)")
        print("[!] Policy Engine updating Istio configurations: IMPLEMENTING MICRO-SEGMENTATION...")
        run_remote_kubectl("kubectl apply -f /root/banking-app/isolate-policy.yaml")
        print("\n=> Refresh the browser now. Istio Mesh should immediately return 'RBAC: access denied'. LATERAL MOVEMENT BLOCKED!")
        time.sleep(2)
        
    elif choice == '3':
        break
    else:
        print("Invalid choice.")
