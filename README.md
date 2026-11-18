# The Claude Handbook: companion code

The code from *The Claude Handbook: The Complete Guide to Working, Writing, and Building with Anthropic's AI* by Daniel Ashgrove.

Each folder holds the files from one chapter, under the same names the chapter uses. Read the chapter first: it explains each file, what to install, how to run it and what you should see. The files here save you typing them in.

| Folder | Chapter | What's in it |
|---|---|---|
| `chapter-13` | Advanced Claude Code: Subagents, Hooks, and Custom Commands | A skill, a subagent, project settings and two hook scripts, in a `.claude` folder |
| `chapter-14` | Claude Code in Practice: Real Projects, Git Workflows, Debugging | Project settings and a `.worktreeinclude` file |
| `chapter-15` | The Claude API: Authentication, Models, and Your First Request | First requests in curl, Python and TypeScript; listing models; a conversation; the first reply drafter; error handling |
| `chapter-16` | Prompt Engineering for Developers | The drafter's system prompt and template, effort and thinking, and the test suite |
| `chapter-17` | Tool Use, Function Calling, and Structured Outputs | The drafter with order-lookup tools, structured output, a grader and the test suite |
| `chapter-18` | Streaming, Batch Processing, and Production Considerations | Prompt caching, streaming, batches and the test suite |
| `chapter-19` | Understanding MCP: The Protocol Behind Claude's Connections | The policy files, project MCP settings, and programs that use an MCP server, locally and remotely |
| `chapter-20` | Building and Deploying Your Own MCP Server | The `shop-orders` MCP server with its tests, a test sign-in script and a Dockerfile, plus programs that use it |
| `chapter-21` | Claude for Teams and Enterprise | An example of managed settings |
| `chapter-22` | Safety, Limits, and Responsible Use | Handling a declined reply, with a test |
| `chapter-23` | Staying Current: How to Keep This Knowledge Up to Date | A check that warns before a model your code uses is retired |

Chapters 1 to 12 work in the Claude app and Claude Code without code of their own, so they have no folder here.

Folders whose names start with a dot, such as `.claude`, are hidden by default on macOS and Linux. Use `ls -a` to see them.

## Before you run anything

- **Your API key stays out of these files.** Set it in the `ANTHROPIC_API_KEY` environment variable, as Chapter 15 shows. Never put it in a file you commit.
- **Each chapter's folder stands on its own.** Chapters 16 to 18 each build on the one before, so their folders share some file names, but each folder holds that chapter's version. Run a chapter's programs from inside its folder.
- **Versions matter.** The code was written for the versions the book names, such as the pinned MCP servers in Chapter 19. Claude and its tools change quickly; Chapter 23 explains how to check what has changed.

## License

MIT. See `LICENSE`.
