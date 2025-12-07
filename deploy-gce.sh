#!/bin/bash
# SVV-LoginPage Google Compute Engine 部署脚本
# 用于性能测试的简化部署

set -e

# ============================================
# 配置变量 (请修改这些值)
# ============================================
PROJECT_ID="your-project-id"        # 改成你的 GCP 项目 ID
ZONE="asia-east1-b"                  # 可选: us-central1-a, europe-west1-b
INSTANCE_NAME="svv-loginpage"
MACHINE_TYPE="e2-medium"             # 性能测试建议用 e2-medium 或更高

# ============================================
# 步骤 1: 创建 VM 实例
# ============================================
echo "Creating Compute Engine instance..."

gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
# 安装 Docker
apt-get update
apt-get install -y docker.io docker-compose git
systemctl start docker
systemctl enable docker

# 克隆项目 (如果是公开仓库)
# git clone https://github.com/YOUR_USERNAME/SVV-LoginPage.git /opt/svv-loginpage
'

echo "VM created successfully!"

# ============================================
# 步骤 2: 配置防火墙规则
# ============================================
echo "Configuring firewall rules..."

gcloud compute firewall-rules create allow-http-8000 \
    --project=$PROJECT_ID \
    --allow=tcp:8000 \
    --target-tags=http-server \
    --description="Allow port 8000 for SVV-LoginPage" \
    2>/dev/null || echo "Firewall rule already exists"

# ============================================
# 步骤 3: 获取外部 IP
# ============================================
echo ""
echo "============================================"
echo "部署完成!"
echo "============================================"
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo ""
echo "VM 外部 IP: $EXTERNAL_IP"
echo ""
echo "下一步操作:"
echo "1. SSH 连接到 VM:"
echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "2. 在 VM 上运行以下命令部署应用:"
echo "   参见下方的 VM 内部署命令"
echo ""
echo "3. 部署后访问:"
echo "   http://$EXTERNAL_IP:8000"
echo "   http://$EXTERNAL_IP:8000/docs"
echo "============================================"
