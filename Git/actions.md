[Core concepts for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/core-concepts-for-github-actions)

## About continuous integration using GitHub Actions

- CI using GitHub Actions offers workflows that can build the code in your repository and run your tests.
- Workflows can run on GitHub-hosted virtual machines, or on machines that you host yourself.

### About GitHub-hosted runners

- Linux, Windows, and macOS operating systems
- You can run workflows directly on the virtual machine or in a Docker container
- GitHub hosts Linux and Windows runners on **Standard_DS2_v2** virtual machines in Microsoft Azure with the GitHub Actions runner application installed.

    |Size|vCPU|Memory:GiB|Temp storage (SSD) GiB|
    |---|---|---|---|
    |Standard_DS2_v2|2|7|14|


### About self-hosted runners

- supported operating systems
    - ubuntu: Ubuntu 16.04 or later
- The self-hosted runner application communicates with GitHub using the HTTPS protocol. You must ensure that the machine has the appropriate network access to communicate with GitHub

`To add a self-hosted runner to a user repository, you must be the repository owner.`

[Adding self-hosted runners](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/adding-self-hosted-runners)

[Using self-hosted runners in a workflow](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/using-self-hosted-runners-in-a-workflow)

## Metadata syntax for GitHub Actions

[Metadata syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions)

## Workflow syntax for GitHub Actions

[Workflow syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idstepswith)

### env

[Using environment variables](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/using-environment-variables)

- `jobs` , `steps` , `전체`
- When more than one environment variable is defined with the same name, GitHub uses the most specific environment variable. For example, an environment variable defined in a step will override job and workflow variables with the same name, while the step executes. A variable defined for a job will override a workflow variable with the same name, while the job executes.
- Environment variables are case-sensitive.
- If you are setting a secret in an environment variable, you must set secrets using the secrets context.

        steps:
          - name: My first action
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

- `on`
    - `<push|pull_request>.<branches|tags>` : When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. (If you only define only tags or only branches, the workflow won't run for events affecting the undefined Git ref?)
    - `<push|pull_request>.paths` : run when at least one file does not match `paths-ignore` or at least one modified file matches the configured `paths` (**.py push 됐을 때만)

    **filter-pattern-cheat-sheet**

    [Workflow syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet)

- `jobs`
    - Jobs run in parallel by default. To run jobs sequentially, you can define dependencies on other jobs using the jobs. `<job_id>.needs` keyword. Each job runs in an environment specified by `runs-on`.
    - 조건문, Job status check functions 등등

    [Contexts and expression syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions)

    - `jobs` 하위에 `steps` 정의
    - `<job_id>.needs` : Identifies any jobs that must complete successfully before this job will run.
    - `<job_id>.runs-on` : Required The type of machine to run the job on. The machine can be either a GitHub-hosted runner, or a self-hosted runner.
    - `<job_id>.if` : You can use the if conditional to prevent a job from running unless a condition is met.
    - `steps`
    - A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Because steps run in their own process, changes to environment variables are not preserved between steps**.** GitHub provides built-in steps to set up and complete a job.
    - `steps.if` :

            steps:
             - name: My first step
               if: github.event_name == 'pull_request' && github.event.action == 'unassigned'
               run: echo This event is a pull request that had an assignee removed.

        - backup step
            ```
            steps:
                - name: My first step
                    # Use an action (`my-action`) in your repository
                    uses: ./.github/actions/my-action
                - name: My backup step
                    if: failure()
                    uses: actions/heroku@master
            ```
    - `[steps.name](http://steps.name)` : A name for your step to display on GitHub.
    - `steps.uses`: Selects an action to run as part of a step in your job. An action is a reusable unit of code. (미리 정해진 템플릿 같은 거 남이 해놓은 액션 가져와서 사용, public repo에 정의된 거만 가능한 거 같음)
    - `[steps.run](http://steps.run)` : Runs command-line programs using the operating system's shell.
        - command & shell
            - A single-line command
                ```
                - name: Install Dependencies
                  run: npm install
                ```
            - A multi-line command:
                ```
                - name: Clean install dependencies and   build
                  run: |
                    npm ci
                    npm run build
                ```
            - Using the working-directory keyword, you can specify the working directory of where to run the command
                ```
                - name: Clean temp directory
                  run: rm -rf *
                  working-directory: ./temp
                ```
            - Example running a script using bash
                ```
                steps:
                  - name: Display the path
                    run: echo $PATH
                    shell: bash
                ```
            - Example running a python script
                ```
                steps:
                  - name: Display the path
                    run: |
                      import os
                      print(os.environ['PATH'])
                    shell: python
                ```
    - `steps.with` : A map of the input parameters defined by the action. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.
        - Example
        - `args` : GitHub passes the args to the container's ENTRYPOINT when the container starts up.
        - `entrypoint` : Overrides the Docker ENTRYPOINT in the Dockerfile
    - `steps.continue-on-error` : Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.

    *container 관련 부분 생략됐으니 container 부분 보고 싶으면 문서 참조