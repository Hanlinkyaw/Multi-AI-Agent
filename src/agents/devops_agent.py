import os
import re
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from ..tools.devops_tools import DevOpsTools, execute_safe_command

class DevOpsAgent(BaseAgent):
    def __init__(self, api_key: Optional[str] = None):
        """
        DevOps agent for infrastructure, deployment, and system administration tasks.
        Specialized in Docker, AWS, Kubernetes, and Linux commands.
        """
        system_prompt = """သင်သည် DevOps Agent ဖြစ်ပါသည်။ သင်၏တာဝန်မှာ DevOps workflows နှင့် infrastructure management ဆိုင်ရာ အကူညီများပေးရန် ဖြစ်သည်။

သင့်ကျွမ်းကျင်သောနယ်ပယ်များ:
- Docker: containerization, images, volumes, networks
- Kubernetes: pods, services, deployments, ingress
- AWS: EC2, S3, Lambda, CloudFormation, VPC
- Linux: system administration, shell commands, troubleshooting
- CI/CD: GitHub Actions, GitLab CI, Jenkins
- Monitoring: logging, metrics, alerting
- Infrastructure as Code: Terraform, Ansible

အသုံးပြုသော language များ:
- Myanmar (မြန်မာဘာသာ) - အဓိက
- English - technical terms များအတွက်

တုံ့ပြန်ပုံစံ:
- Command examples များကို တိကျစွာပေးပါ
- Security best practices များထည့်သွင်းပါ
- Error troubleshooting steps များရှင်းပြပါ
- Production environment အတွက် အကြံပြုချက်များပေးပါ
- Step-by-step instructions များပေးပါ

အရေးကြီးသောစည်းကမ်းချက်များ:
- ဘေးအန္တရာယ်ကင်းရှင်းသော commands များသာ အကြံပြုပါ
- Backup strategies များထည့်သွင်းပါ
- Documentation references များပေးပါ"""
        
        super().__init__(
            name="DevOps Agent",
            system_prompt=system_prompt,
            api_key=api_key
        )
        
        self.devops_tools = DevOpsTools()
    
    def get_agent_type(self) -> str:
        return "devops"
    
    def can_handle(self, message: str) -> bool:
        """
        Check if the message is related to DevOps tasks.
        """
        devops_keywords = [
            # Container & Orchestration
            "docker", "container", "kubernetes", "k8s", "pod", "deployment",
            # Cloud Services
            "aws", "ec2", "s3", "lambda", "cloudformation", "vpc", "azure", "gcp",
            # System Administration
            "server", "deployment", "deploy", "linux", "ubuntu", "centos", "shell",
            "command", "script", "bash", "ssh", "server", "host", "machine",
            # CI/CD
            "ci/cd", "pipeline", "github actions", "gitlab", "jenkins", "build",
            # Infrastructure
            "infrastructure", "terraform", "ansible", "iac", "monitoring", "logging",
            # Myanmar terms
            "ဆာဗာ", "ဒီပလွိုင်း", "ဒေါက်ကာ", "ကွန်တိန်နာ", "ကလောက်", "စက်", "ကွန်ရက်",
            "လုပ်ဆောင်ချက်", "စနစ်", "ကွန်ဖစ်", "မော်နီတာ"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in devops_keywords)
    
    def get_docker_help(self, topic: str) -> str:
        """Get Docker-specific help."""
        docker_commands = {
            "basic": "docker run, docker ps, docker stop, docker rm",
            "images": "docker build, docker push, docker pull, docker images",
            "volumes": "docker volume create, docker volume ls, docker volume rm",
            "networks": "docker network create, docker network ls, docker network connect"
        }
        return docker_commands.get(topic.lower(), "Docker help not available for this topic")
    
    def get_aws_help(self, service: str) -> str:
        """Get AWS service-specific help."""
        aws_services = {
            "ec2": "EC2 instance management, security groups, key pairs",
            "s3": "S3 buckets, objects, permissions, lifecycle policies",
            "lambda": "Lambda functions, triggers, IAM roles",
            "cloudformation": "Stacks, templates, parameters, outputs"
        }
        return aws_services.get(service.lower(), "AWS help not available for this service")
    
    def execute_command(self, command: str) -> Dict[str, any]:
        """Execute a DevOps command safely."""
        return self.devops_tools.execute_command(command)
    
    def get_system_status(self) -> Dict[str, any]:
        """Get comprehensive system status."""
        return {
            "disk_usage": self.devops_tools.get_disk_usage(),
            "memory_usage": self.devops_tools.get_memory_usage(),
            "system_uptime": self.devops_tools.get_system_uptime(),
            "docker_status": self.devops_tools.get_docker_containers()
        }
    
    def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process DevOps-related messages with command execution capabilities.
        """
        if not self.can_handle(message):
            return f"❌ {self.name} အနေဖြင့် ဤ message ကို handle လုပ်နိုင်မည် မဟုတ်ပါ။"
        
        # Check if user wants to execute a command
        command_patterns = [
            r'run\s+(.+)',
            r'execute\s+(.+)',
            r'လုပ်ပါ\s*(.+)',
            r'command\s+(.+)',
            r'cmd\s+(.+)'
        ]
        
        for pattern in command_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                command = match.group(1).strip()
                result = self.execute_command(command)
                
                if result["success"]:
                    return f"✅ Command executed successfully:\n\n```bash\n{command}\n```\n\n**Output:**\n```\n{result['output']}\n```"
                else:
                    return f"❌ Command execution failed:\n\n```bash\n{command}\n```\n\n**Error:** {result.get('error', 'Unknown error')}\n**Reason:** {result.get('reason', 'No reason provided')}"
        
        # Check for system status requests
        if any(keyword in message.lower() for keyword in ["status", "system", "စစ်ဆေး", "အခြေအနေ"]):
            status = self.get_system_status()
            status_text = "🖥️ **System Status**\n\n"
            
            if status["disk_usage"]["success"]:
                status_text += f"**Disk Usage:**\n```\n{status['disk_usage']['output']}\n```\n\n"
            
            if status["memory_usage"]["success"]:
                status_text += f"**Memory Usage:**\n```\n{status['memory_usage']['output']}\n```\n\n"
            
            if status["system_uptime"]["success"]:
                status_text += f"**System Uptime:**\n```\n{status['system_uptime']['output']}\n```\n\n"
            
            if status["docker_status"]["success"]:
                status_text += f"**Docker Containers:**\n```\n{status['docker_status']['output']}\n```\n\n"
            
            return status_text
        
        # Add DevOps context
        devops_context = {
            "specialization": "DevOps & Infrastructure",
            "expertise": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
            "focus": "Production-ready solutions with security best practices",
            "available_commands": self.devops_tools.get_safe_commands_list()[:10]  # Show first 10
        }
        
        if context:
            devops_context.update(context)
        
        return super().process_message(message, devops_context)
