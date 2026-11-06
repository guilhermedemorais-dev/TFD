# Public code discovery

Use during Discovery/SDD only when a concrete unresolved question benefits
from an external implementation example. Reuse project sources and recorded
research first. Ordinary source search does not require reverse-engineering
runtime tools. SDD owns interpretation; implementation and QA retain validation.

Consult applicable [backend candidates](backend-component-sources.md) metadata
after native sources and before new implementation searches; retain the same
project source ID and provenance. Nonselected candidates do not become REQUIRED.

## Search and availability

The [official Grep documentation](https://vercel.com/blog/grep-a-million-github-repositories-via-mcp)
describes the public GitHub code index at [grep.app](https://grep.app) and its
HTTP MCP endpoint `https://mcp.grep.app`, with literal/regex search and language,
repository and path filters. It is distinct from community `grep-mcp` wrappers.

Discover current host tools before choosing a route. Prefer the official Grep
MCP when connected and demonstrably available. Discover its actual tool schema;
do not invent tool names or assume catalog/config presence proves availability.
If absent, use available GitHub code tools, the public search website or bounded
official-source research. If none can answer the question, report that limit.
Do not block unrelated specification work because an optional search is absent.
Do not install/connect a server silently; route requested preparation through
the existing Environment Bootstrap, preserving its consent and host checks.

Search concrete public symbols or patterns and refine with relevant filters.
Use generic queries; do not send private code, secrets, customer data or
unapproved internal identifiers to a public index. Stop when the question is
answered; do not repeat repository-wide research for each module.

## Verify candidates before reuse

Search results are candidates, not validated code. For a selected candidate:

1. Open the original repository/file and capture the exact commit/release,
   source URL, relevant symbols and the question it answers.
2. Read surrounding implementation, dependencies and related tests; distinguish
   production behavior from examples, stubs, mocks or obsolete APIs.
3. Verify the applicable license and attribution terms before copying code.
   Unknown/incompatible rights prevent copying; choose another candidate or
   specify independently from authoritative documented behavior.
4. Check compatibility with the approved stack, versions, contracts and security
   requirements. Do not choose architecture merely because a result uses it.
5. Record in the existing reference library and `REUSE_INVENTORY`: origin,
   revision, purpose, adoption/adaptation/rejection, limits and planned tests.
   Keep FOUND/INSPECTED distinct from TESTED in the target environment.

Discovery does not run unknown software or import dependencies. Route approved
adaptation through implementation and the existing independent validators.
Upstream tests/stars do not prove correctness or safety in the client system;
mark unexecuted target validation NOT VALIDATED. No guaranteed time saving is
implied by adding this search route.
