# Flux Capacitor
Commit to a repository daily — ensuring a consistent and uninterrupted commit streak.

## Requirements
`pip install -r requirements.txt`

## Setup
These steps ensure a robust setup for managing your GitHub repository effectively, integrating automated daily commits seamlessly into your workflow.

1. **Git Configuration**: Ensure your system is authenticated with Git for seamless operation.
2. **Download and Repository Creation**: Begin by cloning this repository and creating your own fork on GitHub.
3. **Initial Commit**: Prioritize committing the `history.json` file as the first step before initiating daily commits.

> **Important**: Upon completing the repository setup and Git configuration, the next critical step involves establishing a daily commit routine. The script automates updates and processing, simplifying the process significantly; and it can also loop infinitely to act as a meta-cronjob, however, it is recommended to make your own cronjob/scheduled task.

### Possible Bugs
While the setup is straightforward, there are potential issues that may arise:

1. **Commit Failures**: In case of commit failures, consider re-cloning or merging the repository on your local machine.
    > **Note**: This has mostly been remedied by pulling the repo before committing any updates, however, it's possible it could still fail.
2. **Git Configuration**: Resolve any Git configuration issues by generating a GitHub token through developer settings and ensuring it is properly configured on your system.

## Resources
**Setting Up Git**
- https://docs.github.com/en/get-started/getting-started-with-git/set-up-git

**Caching Github Crendentials**
- https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git