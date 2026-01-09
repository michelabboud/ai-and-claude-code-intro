#!/bin/bash
# Chapter 10: AI for DevOps
# Shell Aliases and Functions for AI-Assisted DevOps
#
# Add these to your ~/.bashrc or ~/.zshrc

# =============================================================================
# BASIC ALIASES
# =============================================================================

# Quick Claude queries
alias ai='claude'
alias aihelp='claude "/help"'

# Code review shortcut
alias aireview='claude "Review this file for issues: "'

# Quick debugging
alias aidebug='claude "Help me debug this error: "'

# Generate from template
alias aigen='claude "/generate "'

# Explain code
alias aiexplain='claude "Explain what this code does: "'

# =============================================================================
# FUNCTIONS FOR COMMON DEVOPS TASKS
# =============================================================================

# Review current PR changes
ai-review-pr() {
    local base_branch="${1:-main}"
    git diff "origin/${base_branch}...HEAD" | claude "Review these changes for:
    1. Security issues
    2. Performance problems
    3. Best practice violations
    4. Missing error handling

    Format findings by severity (Critical, Major, Minor)."
}

# Generate commit message from staged changes
ai-commit() {
    local staged_diff=$(git diff --staged)
    if [ -z "$staged_diff" ]; then
        echo "No staged changes found. Stage changes with 'git add' first."
        return 1
    fi

    echo "$staged_diff" | claude "Write a conventional commit message for these changes.
    Format: <type>(<scope>): <description>
    Types: feat, fix, docs, style, refactor, test, chore
    Keep it under 72 characters."
}

# Analyze logs for issues
ai-logs() {
    local log_file="${1:-/var/log/syslog}"
    local lines="${2:-100}"

    tail -n "$lines" "$log_file" | claude "Analyze these logs and:
    1. Identify any errors or warnings
    2. Summarize the main events
    3. Highlight anything that needs attention
    4. Suggest next steps if issues found"
}

# Debug Kubernetes pod
ai-k8s-debug() {
    local pod_name="$1"
    local namespace="${2:-default}"

    if [ -z "$pod_name" ]; then
        echo "Usage: ai-k8s-debug <pod-name> [namespace]"
        return 1
    fi

    kubectl describe pod "$pod_name" -n "$namespace" | claude "Analyze this pod description:
    1. Identify any issues (CrashLoopBackOff, ImagePullBackOff, etc.)
    2. Check resource constraints
    3. Review events for problems
    4. Suggest troubleshooting steps"
}

# Analyze Terraform plan
ai-terraform-plan() {
    terraform plan -out=tfplan 2>&1 | claude "Analyze this Terraform plan:
    1. Summarize what will be created, modified, destroyed
    2. Highlight any risky changes
    3. Check for potential cost implications
    4. Verify security configurations"
}

# Generate Kubernetes manifest
ai-k8s-generate() {
    local service_name="$1"
    local image="$2"
    local port="${3:-8080}"

    if [ -z "$service_name" ] || [ -z "$image" ]; then
        echo "Usage: ai-k8s-generate <service-name> <image> [port]"
        return 1
    fi

    claude "Generate production-ready Kubernetes manifests for:
    Service: $service_name
    Image: $image
    Port: $port

    Include:
    - Deployment with 3 replicas
    - Service (ClusterIP)
    - HPA (2-10 replicas, 70% CPU target)
    - Resource limits
    - Health probes
    - PodDisruptionBudget"
}

# Explain error message
ai-error() {
    local error_msg="$*"
    if [ -z "$error_msg" ]; then
        echo "Usage: ai-error <error message>"
        return 1
    fi

    claude "Explain this error and how to fix it:
    $error_msg

    Include:
    1. What the error means
    2. Common causes
    3. Step-by-step fix
    4. Prevention tips"
}

# Security scan helper
ai-security-scan() {
    local file_or_dir="${1:-.}"

    if [ -f "$file_or_dir" ]; then
        cat "$file_or_dir" | claude "Security review this code for:
        1. OWASP Top 10 vulnerabilities
        2. Hardcoded secrets or credentials
        3. Injection risks
        4. Authentication/authorization issues
        5. Data exposure risks"
    else
        find "$file_or_dir" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) -print0 | \
            xargs -0 cat | head -c 50000 | claude "Security review these code files for:
        1. OWASP Top 10 vulnerabilities
        2. Hardcoded secrets
        3. Injection risks"
    fi
}

# Docker image analysis
ai-docker-analyze() {
    local dockerfile="${1:-Dockerfile}"

    if [ ! -f "$dockerfile" ]; then
        echo "Dockerfile not found: $dockerfile"
        return 1
    fi

    cat "$dockerfile" | claude "Analyze this Dockerfile for:
    1. Security best practices
    2. Image size optimization
    3. Layer caching efficiency
    4. Multi-stage build opportunities
    5. Specific improvements with code examples"
}

# Quick documentation generator
ai-docs() {
    local file="$1"

    if [ -z "$file" ] || [ ! -f "$file" ]; then
        echo "Usage: ai-docs <file>"
        return 1
    fi

    cat "$file" | claude "Generate documentation for this code:
    1. Overview of what it does
    2. Function/class descriptions
    3. Usage examples
    4. Dependencies and requirements

    Format as markdown suitable for a README."
}

# =============================================================================
# INTERACTIVE HELPERS
# =============================================================================

# Start an AI DevOps session with context
ai-devops-session() {
    echo "Starting AI DevOps session..."
    echo "Gathering project context..."

    local context=""

    # Add git context if in a repo
    if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        context+="Git branch: $(git branch --show-current)\n"
        context+="Recent commits:\n$(git log --oneline -5)\n"
        context+="Uncommitted changes: $(git status --short | wc -l) files\n"
    fi

    # Add K8s context if kubectl available
    if command -v kubectl &> /dev/null; then
        context+="K8s context: $(kubectl config current-context 2>/dev/null || echo 'not configured')\n"
    fi

    # Add AWS context if configured
    if [ -n "$AWS_PROFILE" ]; then
        context+="AWS profile: $AWS_PROFILE\n"
    fi

    echo -e "Context:\n$context"
    echo ""
    echo "Starting Claude Code with project context..."

    claude "You are my DevOps assistant. Here's the current context:
    $context

    How can I help you today?"
}

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

# Show available prompt templates
ai-templates() {
    cat << 'EOF'
Available AI prompt templates:

TROUBLESHOOTING:
  ai-error <message>     - Explain and fix an error
  ai-logs <file> [n]     - Analyze last n lines of logs
  ai-k8s-debug <pod>     - Debug Kubernetes pod

CODE REVIEW:
  ai-review-pr [branch]  - Review PR changes
  aireview <file>        - Quick file review
  ai-security-scan       - Security scan code

GENERATION:
  ai-commit              - Generate commit message
  ai-k8s-generate        - Generate K8s manifests
  ai-docs <file>         - Generate documentation
  ai-docker-analyze      - Analyze Dockerfile

INFRASTRUCTURE:
  ai-terraform-plan      - Analyze terraform plan

INTERACTIVE:
  ai-devops-session      - Start contextual session

Use 'type <function>' to see the implementation.
EOF
}

# Print this on shell startup
echo "AI DevOps aliases loaded. Type 'ai-templates' for available commands."
