---
name: github-issues
description: Technical guide for GitHub Issues management with gh CLI
---

# GitHub Issues Management - Technical Reference

Technical reference for managing GitHub Issues using `gh` CLI.

## Prerequisites

```bash
# Install gh CLI
brew install gh  # macOS
sudo apt install gh  # Linux

# Authenticate
gh auth login

# Verify authentication
gh auth status
```

## Creating Issues

### Basic Issue Creation
```bash
gh issue create \
  --repo OWNER/REPO \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --label "label1,label2"
```

### Interactive Creation
```bash
gh issue create --repo OWNER/REPO --web
```

### With Full Options
```bash
gh issue create \
  --repo OWNER/REPO \
  --title "Issue Title" \
  --body "Detailed description" \
  --label "bug,priority:high" \
  --assignee USERNAME \
  --milestone "v1.0" \
  --project "PROJECT_NAME"
```

### Capturing Issue URL
```bash
ISSUE_URL=$(gh issue create \
  --repo OWNER/REPO \
  --title "Title" \
  --body "Description" \
  --format json | jq -r '.url')

echo "Created: $ISSUE_URL"
```

## Viewing Issues

```bash
# List all open issues
gh issue list --repo OWNER/REPO

# List with filters
gh issue list --repo OWNER/REPO --state open
gh issue list --repo OWNER/REPO --state closed
gh issue list --repo OWNER/REPO --label "bug"
gh issue list --repo OWNER/REPO --assignee @me
gh issue list --repo OWNER/REPO --assignee USERNAME

# View specific issue
gh issue view ISSUE_NUMBER --repo OWNER/REPO

# View with comments
gh issue view ISSUE_NUMBER --repo OWNER/REPO --comments

# View in browser
gh issue view ISSUE_NUMBER --repo OWNER/REPO --web
```

## Editing Issues

### Edit Title
```bash
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --title "NEW_TITLE"
```

### Edit Body
```bash
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --body "NEW_DESCRIPTION"
```

### Manage Labels
```bash
# Add label
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-label "bug"

# Remove label
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --remove-label "bug"

# Replace all labels
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --label "bug,priority:high"
```

### Manage Assignees
```bash
# Add assignee
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-assignee USERNAME
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-assignee @me

# Remove assignee
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --remove-assignee USERNAME
```

### Set Milestone
```bash
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --milestone "v1.0"
```

### Add to Project
```bash
gh issue edit ISSUE_NUMBER --repo OWNER/REPO --add-project "PROJECT_NAME"
```

## Closing and Reopening Issues

```bash
# Close issue
gh issue close ISSUE_NUMBER --repo OWNER/REPO

# Close with comment
gh issue close ISSUE_NUMBER --repo OWNER/REPO --comment "Fixed in PR #123"

# Close with reason
gh issue close ISSUE_NUMBER --repo OWNER/REPO --reason "completed"
gh issue close ISSUE_NUMBER --repo OWNER/REPO --reason "not planned"

# Reopen issue
gh issue reopen ISSUE_NUMBER --repo OWNER/REPO
```

## Comments

```bash
# Add comment
gh issue comment ISSUE_NUMBER --repo OWNER/REPO --body "Comment text"

# Edit comment (interactive)
gh issue comment ISSUE_NUMBER --repo OWNER/REPO --edit

# Comment in browser
gh issue comment ISSUE_NUMBER --repo OWNER/REPO --web
```

## Project Board Integration

### Add Issue to Project
```bash
# By project ID
gh project item-add PROJECT_ID \
  --owner OWNER \
  --url https://github.com/OWNER/REPO/issues/NUMBER

# Example
gh project item-add 5 \
  --owner TheRealKoller \
  --url https://github.com/TheRealKoller/cookidoo-assistant/issues/42
```

### List Project Items
```bash
gh project item-list PROJECT_ID --owner OWNER --format json
```

### Edit Project Item
```bash
gh project item-edit \
  --id ITEM_ID \
  --project-id PROJECT_ID \
  --owner OWNER \
  --field-id FIELD_ID \
  --text "STATUS"
```

## Search and Filter

```bash
# Search by keyword
gh issue list --repo OWNER/REPO --search "keyword"

# Complex search
gh issue list --repo OWNER/REPO --search "is:open label:bug assignee:@me"

# JSON output for processing
gh issue list --repo OWNER/REPO --json number,title,state,labels --jq '.'
```

## Batch Operations

### Create Multiple Issues
```bash
for title in "Issue 1" "Issue 2" "Issue 3"; do
  gh issue create \
    --repo OWNER/REPO \
    --title "$title" \
    --label "enhancement"
done
```

### Add Label to Multiple Issues
```bash
gh issue list --repo OWNER/REPO --state open --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --repo OWNER/REPO --add-label "needs-review"
```

### Close Multiple Issues
```bash
for num in 10 11 12; do
  gh issue close $num --repo OWNER/REPO --comment "Batch closed"
done
```

## Output Formats

```bash
# JSON output
gh issue list --repo OWNER/REPO --json number,title,state,labels

# Custom template
gh issue list --repo OWNER/REPO --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'

# JQ processing
gh issue list --repo OWNER/REPO --json number,title,labels --jq '.[] | select(.labels[].name == "bug")'
```

## Permission Management

### Check Authentication
```bash
gh auth status
```

### Refresh Authentication
```bash
# Add specific scope
gh auth refresh -s repo
gh auth refresh -s project

# Multiple scopes
gh auth refresh -s repo -s project -s workflow
```

### Re-authenticate with Scopes
```bash
gh auth login --scopes repo,project,workflow
```

### Common Scopes
- `repo` - Full repository access
- `project` - Project board access
- `workflow` - GitHub Actions workflow access
- `admin:org` - Organization administration

## Troubleshooting

### Issue Not Found
```bash
# Verify issue exists
gh issue list --repo OWNER/REPO --search "NUMBER"

# Check if you have access
gh auth status
```

### Permission Denied
```bash
# Refresh with required scope
gh auth refresh -s repo -s project

# Or re-authenticate
gh auth login --scopes repo,project
```

### Rate Limiting
```bash
# Check rate limit status
gh api rate_limit

# Wait or use authenticated requests (higher limit)
```

### Finding Item ID
```bash
# List all project items and filter
gh project item-list PROJECT_ID --owner OWNER --format json | \
  jq '.items[] | select(.content.title | contains("SEARCH_TERM"))'
```

## Advanced Examples

### Create Issue and Add to Project in One Command
```bash
ISSUE_URL=$(gh issue create \
  --repo OWNER/REPO \
  --title "Title" \
  --body "Description" \
  --label "label" \
  --format json | jq -r '.url') && \
gh project item-add PROJECT_ID --owner OWNER --url "$ISSUE_URL"
```

### Export Issues to CSV
```bash
gh issue list --repo OWNER/REPO --state all --json number,title,state,labels,createdAt \
  --jq '.[] | [.number, .title, .state, (.labels | map(.name) | join(";")), .createdAt] | @csv'
```

### Find Issues by Date Range
```bash
gh issue list --repo OWNER/REPO \
  --search "created:2024-01-01..2024-12-31" \
  --json number,title,createdAt
```

## References

- [gh issue documentation](https://cli.github.com/manual/gh_issue)
- [gh project documentation](https://cli.github.com/manual/gh_project)
- [GitHub search syntax](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
