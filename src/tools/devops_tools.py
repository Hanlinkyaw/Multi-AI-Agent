import subprocess
import os
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum

class CommandSafety(Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGEROUS = "dangerous"
    FORBIDDEN = "forbidden"

class DevOpsTools:
    """
    Safe shell command execution for DevOps operations.
    Provides controlled access to system commands with safety checks.
    """
    
    # Safe commands that can be executed
    SAFE_COMMANDS = {
        # System information
        'df', 'free', 'uname', 'uptime', 'whoami', 'id', 'date', 'hostname',
        # File system (read-only)
        'ls', 'find', 'cat', 'head', 'tail', 'wc', 'grep', 'du', 'tree',
        # Process information
        'ps', 'top', 'htop',
        # Network (read-only)
        'ping', 'netstat', 'ss', 'ip', 'ifconfig',
        # Docker (safe operations)
        'docker', 'docker-compose',
        # Package management (read-only)
        'apt-cache', 'yum', 'dnf', 'pip', 'npm', 'cargo',
        # System services (read-only)
        'systemctl', 'service', 'journalctl'
    }
    
    # Dangerous commands that are forbidden
    FORBIDDEN_COMMANDS = {
        # System destruction
        'rm', 'rmdir', 'dd', 'mkfs', 'fdisk', 'format',
        # User management
        'useradd', 'userdel', 'usermod', 'passwd', 'chown', 'chmod',
        # System configuration
        'reboot', 'shutdown', 'halt', 'poweroff',
        # Package installation/removal
        'apt', 'yum', 'dnf', 'pacman', 'apk',
        # Network configuration
        'iptables', 'ufw', 'firewalld',
        # System files
        'sudo', 'su', 'visudo', 'crontab',
        # Shell scripting
        'sh', 'bash', 'zsh', 'fish', 'eval', 'exec'
    }
    
    def __init__(self):
        self.command_history: List[Dict[str, str]] = []
    
    def check_command_safety(self, command: str) -> Tuple[CommandSafety, str]:
        """
        Check if a command is safe to execute.
        
        Args:
            command: Command to check
            
        Returns:
            Tuple of (safety_level, reason)
        """
        # Extract base command (first word)
        base_command = command.split()[0].strip()
        
        # Check if command is forbidden
        if base_command in self.FORBIDDEN_COMMANDS:
            return CommandSafety.FORBIDDEN, f"Command '{base_command}' is forbidden for security reasons"
        
        # Check if command is in safe list
        if base_command in self.SAFE_COMMANDS:
            return CommandSafety.SAFE, f"Command '{base_command}' is safe to execute"
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r';\s*rm\s+',  # rm after semicolon
            r'\|\s*rm\s+',  # rm after pipe
            r'&&\s*rm\s+',  # rm after &&
            r'\$\(.*rm.*\)',  # rm in command substitution
            r'`.*rm.*`',  # rm in backticks
            r'/dev/',  # device file access
            r'etc/passwd',  # system file access
            r'etc/shadow',  # password file access
            r'~/.ssh/',  # SSH keys access
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return CommandSafety.DANGEROUS, f"Command contains dangerous pattern: {pattern}"
        
        # Unknown command - treat as warning
        return CommandSafety.WARNING, f"Command '{base_command}' is not in the safe list"
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, any]:
        """
        Execute a shell command safely.
        
        Args:
            command: Command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Dictionary with execution results
        """
        safety_level, safety_reason = self.check_command_safety(command)
        
        if safety_level == CommandSafety.FORBIDDEN:
            return {
                "success": False,
                "error": "Command forbidden",
                "reason": safety_reason,
                "command": command,
                "output": "",
                "return_code": -1
            }
        
        try:
            # Execute the command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            # Log the command
            log_entry = {
                "command": command,
                "return_code": result.returncode,
                "safety_level": safety_level.value,
                "timestamp": str(subprocess.run(['date'], capture_output=True, text=True).stdout.strip())
            }
            self.command_history.append(log_entry)
            
            return {
                "success": result.returncode == 0,
                "command": command,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "safety_level": safety_level.value,
                "safety_reason": safety_reason
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout",
                "reason": f"Command exceeded {timeout} seconds timeout",
                "command": command,
                "output": "",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Execution error",
                "reason": str(e),
                "command": command,
                "output": "",
                "return_code": -1
            }
    
    def get_disk_usage(self) -> Dict[str, any]:
        """Get disk usage information."""
        return self.execute_command("df -h")
    
    def get_memory_usage(self) -> Dict[str, any]:
        """Get memory usage information."""
        return self.execute_command("free -h")
    
    def get_docker_containers(self) -> Dict[str, any]:
        """Get running Docker containers."""
        return self.execute_command("docker ps")
    
    def get_docker_images(self) -> Dict[str, any]:
        """Get Docker images."""
        return self.execute_command("docker images")
    
    def get_system_uptime(self) -> Dict[str, any]:
        """Get system uptime."""
        return self.execute_command("uptime")
    
    def get_running_processes(self) -> Dict[str, any]:
        """Get running processes."""
        return self.execute_command("ps aux")
    
    def get_network_connections(self) -> Dict[str, any]:
        """Get network connections."""
        return self.execute_command("netstat -tuln")
    
    def get_command_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent command history."""
        return self.command_history[-limit:]
    
    def clear_history(self):
        """Clear command history."""
        self.command_history.clear()
    
    def get_safe_commands_list(self) -> List[str]:
        """Get list of safe commands."""
        return sorted(list(self.SAFE_COMMANDS))
    
    def get_forbidden_commands_list(self) -> List[str]:
        """Get list of forbidden commands."""
        return sorted(list(self.FORBIDDEN_COMMANDS))


# Convenience functions for common DevOps operations
def check_system_status() -> Dict[str, any]:
    """Get comprehensive system status."""
    tools = DevOpsTools()
    
    status = {
        "disk_usage": tools.get_disk_usage(),
        "memory_usage": tools.get_memory_usage(),
        "system_uptime": tools.get_system_uptime(),
        "running_processes": tools.get_running_processes()
    }
    
    return status

def check_docker_status() -> Dict[str, any]:
    """Get Docker status information."""
    tools = DevOpsTools()
    
    status = {
        "containers": tools.get_docker_containers(),
        "images": tools.get_docker_images()
    }
    
    return status

def execute_safe_command(command: str) -> Dict[str, any]:
    """Execute a command with safety checks."""
    tools = DevOpsTools()
    return tools.execute_command(command)
