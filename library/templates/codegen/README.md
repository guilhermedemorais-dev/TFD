# Project-owned generator fallback

Use a native stack generator or existing reusable component first. Select Plop
only for repeated project patterns when that option does not fit. Plop generates
files from reviewed templates; it does not enforce architecture or guarantee
Clean Code. The sector approves paths, exports, state, styling and test conventions
against actual project examples before adopting a template. This is an optional
starter resource, not a new application or mandatory structure.

## JavaScript/JSX starter

`react-js/plopfile.cjs` registers a minimal named component generator, without
TypeScript or React package installation. React 19 projects support this pattern;
no library-version upgrade is implied. It writes only
`src/components/<Name>/<Name>.jsx` under the explicitly selected current project
and rejects non-PascalCase identifiers, including path separators. Existing files
are not overwritten by its add action. Inspect the target for unexpected symlinks
and use only a controlled project checkout.

After adapting the template once to that project's verified conventions, install
an exact compatible Plop version as a project dev dependency using the shared
CLI policy. Invoke its local binary or package script, with cwd set to the approved
project and `--plopfile` pointing to the adopted file. Example, for a locally
installed Plop, from that project:

```bash
./node_modules/.bin/plop --plopfile <absolute-adopted-plopfile.cjs> react-component -- --name CustomerCard
```

Use the Windows package-script equivalent when needed. This is not a global shell
installation or permission to generate into the Harness repository. Never pass
`--force`. The AI implements only the requested specific logic afterward; run the
project formatter/linter and relevant checks, review the diff and keep generators
versioned with the project. Do not create a separate template for every one-off
edit. No arbitrary business rules, API, container or service is generated here.

## React/Vite and Tailwind

For an approved new JavaScript/JSX application, select Vite's `react` template;
`react-ts` is the TypeScript variant. Preserve the actual approved React major.
For existing applications use their current setup instead of recreating it.
Catalog entries `tailwind-vite` and `tailwind-cli` are alternatives. For Tailwind
v4/Vite prefer the plugin, preserve the React plugin, and add the CSS import per
selected-version official docs. Do not run a second CSS watcher by default or
apply v3 initialization commands to v4.
