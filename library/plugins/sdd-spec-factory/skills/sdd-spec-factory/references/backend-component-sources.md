# Backend component sources

Curated candidate metadata for applicable PRD/spec decisions, not installed tools
or standalone skills. Reuse project-native code first, then matching-stack catalog
candidates, then targeted official-source research for gaps. Record consultation,
selected project source ID/native reuse or justified N/A in existing references.
Only selected necessary source bodies become REQUIRED. Resolve source ownership
from the active SDD bundle, never guessed sibling cache paths.

All entries: source checked 2026-10-14; CANDIDATE, NOT_INSTALLED and target-runtime
NOT_VALIDATED. Source commits below identify inspected default branches, not
published releases, production support or selected dependency versions. Check
project PHP/Node/framework versions, release-specific requirements, lockfiles,
license/subtree and actual tests before approved project-local adoption. No
installation, framework migration, architecture selection, OS certification or
security audit follows from catalog membership. Skills remain OS-neutral.

For applicable blockchain/client/contract-development choices, consult
[Web3 component sources](web3-component-sources.md) metadata; no blockchain
execution or installed runtime is implied.

## Free-edition eligibility

Eligible entries use a zero-license-fee OSI-licensed core/edition. Select only that
free edition and necessary compatible dependencies; paid-only features, assets
and commercial editions are excluded. Copyleft remains conditional on compatible
project/distribution obligations, not blanket permission for proprietary reuse.
Free library code does not imply free infrastructure, support or provider services.
Payment SDK code may be free while transactions/API services incur charges.
No purchase, account setup or provider execution is authorized by this catalog.

Medusa eligibility covers MIT core only, excluding Enterprise Materials. Vendure
eligibility covers its free GPL core only; commercial VCL is not selected.
Liquibase current Community5 FSL-1.1-ALv2 is excluded from eligible candidates:
it is source-available with restrictions rather than this catalog's eligible OSI edition.
This exclusion does not mean all FSL-permitted uses require payment.
[Excluded-source license](https://github.com/liquibase/liquibase/blob/f58ccf20b2610fd04ebcabc943842f1d6484402d/LICENSE.txt).
No historical release is silently substituted or selected.

## Laravel packages (10)

| Stable library ID | Package and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `laravel-fortify` | `laravel/fortify`: Headless Laravel authentication backend; not standalone frontend | [Repo](https://github.com/laravel/fortify), [docs](https://laravel.com/docs/fortify) | MIT |
| `spatie-permission` | `spatie/laravel-permission`: Role/permission authorization integrated with Laravel policies/guards | [Repo](https://github.com/spatie/laravel-permission), [docs](https://spatie.be/docs/laravel-permission) | MIT |
| `spatie-activitylog` | `spatie/laravel-activitylog`: Model activity event logging; not immutable/tamper-proof audit ledger | [Repo](https://github.com/spatie/laravel-activitylog), [docs](https://docs.spatie.be/laravel-activitylog) | MIT |
| `spatie-medialibrary` | `spatie/laravel-medialibrary`: Media/file association and conversions; storage/queue/image prerequisites | [Repo](https://github.com/spatie/laravel-medialibrary), [docs](https://spatie.be/docs/laravel-medialibrary) | MIT |
| `spatie-query-builder` | `spatie/laravel-query-builder`: Allowed API filter/sort/include query construction; enforce explicit allowlists | [Repo](https://github.com/spatie/laravel-query-builder), [docs](https://spatie.be/docs/laravel-query-builder) | MIT |
| `laravel-excel` | `maatwebsite/excel`: Spreadsheet import/export; versioned PhpSpreadsheet and memory/queue concerns | [Repo](https://github.com/SpartnerNL/Laravel-Excel), [docs](https://laravel-excel.com) | MIT |
| `laravel-dompdf` | `barryvdh/laravel-dompdf`: Laravel Dompdf integration for server PDF; not browser-equivalent renderer | [Repo](https://github.com/barryvdh/laravel-dompdf), [docs](https://github.com/barryvdh/laravel-dompdf/blob/a7f7e228b91d95f8dde56e1cff236f15713bb0f0/README.md) | MIT |
| `brick-money` | `brick/money`: Decimal/currency money value objects and allocation; not payment processor | [Repo](https://github.com/brick/money), [docs](https://github.com/brick/money/blob/93f145c6c9f5b58160e2967088e7e083722e28cc/README.md) | MIT |
| `laravel-wallet` | `bavix/laravel-wallet`: Application balances/transfers ledger; not bank, escrow, regulated wallet or reconciliation guarantee | [Repo](https://github.com/bavix/laravel-wallet), [docs](https://github.com/bavix/laravel-wallet/blob/7587df628b377f11accac4b48bb6eac576e5268b/README.md) | MIT |
| `filament` | `filament/filament`: PHP Livewire admin/application panels; separate from Next.js public frontend | [Repo](https://github.com/filamentphp/filament), [docs](https://github.com/filamentphp/filament/blob/0747e62838adcff87b00706ed94a3ed91c46929f/README.md) | MIT |

## Provider/payment and fiscal SDKs (7)

| Stable library ID | Package and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `efi-php` | `efipay/sdk-php-apis-efi`: Official Efi PHP payment API SDK | [Repo](https://github.com/efipay/sdk-php-apis-efi), [docs](https://github.com/efipay/sdk-php-apis-efi/blob/b3996b7c9bcd35acba6127e04d07db0dc9778253/README.md) | MIT |
| `efi-node` | `sdk-node-apis-efi`: Official Efi Node payment API SDK | [Repo](https://github.com/efipay/sdk-node-apis-efi), [docs](https://github.com/efipay/sdk-node-apis-efi/blob/d742ee94b76097383c42792494351a68568e23a9/README.md) | MIT |
| `mercadopago-php` | `mercadopago/dx-php`: Official MercadoPago PHP server SDK | [Repo](https://github.com/mercadopago/sdk-php), [docs](https://github.com/mercadopago/sdk-php/blob/c5fd9086604c41507b45dfbebab057ba288f19c1/README.md) | MIT |
| `mercadopago-node` | `mercadopago`: Official MercadoPago Node server SDK, distinct from browser sdk-js | [Repo](https://github.com/mercadopago/sdk-nodejs), [docs](https://github.com/mercadopago/sdk-nodejs/blob/bf920b9415ba19986b7ffdbf83a5aa21b589a6e0/README.md) | MIT |
| `cashier-stripe` | `laravel/cashier`: Laravel Stripe subscription billing, not general Brazilian fiscal/payment adapter | [Repo](https://github.com/laravel/cashier-stripe), [docs](https://github.com/laravel/cashier-stripe/blob/d8df4daff7a29252ff4ec0298a5364d3bda81ab1/README.md) | MIT |
| `nfephp-sped-nfe` | `nfephp-org/sped-nfe`: Brazilian NFe/NFCe XML signing and SEFAZ integration; not all tax document types | [Repo](https://github.com/nfephp-org/sped-nfe), [docs](https://github.com/nfephp-org/sped-nfe/blob/346c14d5b7e59ab9aab92e7a77c499a19d462fba/README.md) | LGPL-3.0-or-later OR MIT |
| `nfephp-sped-da` | `nfephp-org/sped-da`: Auxiliary fiscal document PDF/DANFE rendering; not SEFAZ authorization | [Repo](https://github.com/nfephp-org/sped-da), [docs](https://github.com/nfephp-org/sped-da/blob/308abfe0fe01a3a2c9acfc7b57bf59fcffc77717/README.md) | LGPL-3.0-or-later OR MIT |


## Node/TypeScript packages (7)

| Stable library ID | Package and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `better-auth` | `better-auth`: Server authentication/session integration | [Repo](https://github.com/better-auth/better-auth), [docs](https://better-auth.com/docs/integrations/next) | MIT |
| `casl` | `@casl/ability`: Isomorphic permissions with server enforcement | [Repo](https://github.com/stalniy/casl), [docs](https://casl.js.org/) | MIT |
| `bullmq` | `bullmq`: Redis-backed jobs and persistent Node workers | [Repo](https://github.com/taskforcesh/bullmq), [docs](https://docs.bullmq.io/guide/connections) | MIT |
| `zod` | `zod`: Runtime schema validation | [Repo](https://github.com/colinhacks/zod), [docs](https://zod.dev) | MIT |
| `exceljs` | `exceljs`: Spreadsheet generation and import | [Repo](https://github.com/exceljs/exceljs), [docs](https://github.com/exceljs/exceljs#browser) | MIT |
| `pdfkit` | `pdfkit`: Programmatic PDF generation | [Repo](https://github.com/foliojs/pdfkit), [docs](https://pdfkit.org/docs/getting_started.html) | MIT |
| `nodemailer` | `nodemailer`: Server SMTP email transport | [Repo](https://github.com/nodemailer/nodemailer), [docs](https://nodemailer.com/smtp) | MIT-0 |

## Commerce platforms (3)

| Stable library ID | Package and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `bagisto` | `bagisto/bagisto`: Laravel commerce application | [Repo](https://github.com/bagisto/bagisto), [docs](https://devdocs.bagisto.com/) | MIT |
| `medusa` | `@medusajs/medusa`: Modular Node commerce platform | [Repo](https://github.com/medusajs/medusa), [docs](https://docs.medusajs.com/) | MIT free core only; Enterprise excluded |
| `vendure` | `@vendure/core`: TypeScript/NestJS/GraphQL headless commerce | [Repo](https://github.com/vendurehq/vendure), [docs](https://docs.vendure.io/) | GPL-3.0-or-later free core only; commercial VCL not selected; plugin exception |

## JavaScript server frameworks and data access (6)

JavaScript and Java are different language/runtime families. Express/Fastify are
Node JavaScript server frameworks with TypeScript support; Nest is TypeScript-first
Node application architecture. Prisma/Drizzle are database tools, not HTTP servers.

| Stable library ID | Package and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `nextjs` | `next`: React application framework with rendering and optional server/BFF adapters | [Repo](https://github.com/vercel/next.js), [docs](https://nextjs.org/docs) | MIT |
| `express` | `express`: Node HTTP server framework | [Repo](https://github.com/expressjs/express), [docs](https://expressjs.com/) | MIT |
| `fastify` | `fastify`: Node HTTP server framework with schema hooks | [Repo](https://github.com/fastify/fastify), [docs](https://fastify.dev/docs/latest/) | MIT |
| `nestjs` | `@nestjs/core`: TypeScript-first Node application framework | [Repo](https://github.com/nestjs/nest), [docs](https://docs.nestjs.com/) | MIT |
| `prisma` | `prisma; @prisma/client (v7), version-specific v8 packages`: Generated database client and ORM tooling | [Repo](https://github.com/prisma/orm), [docs](https://www.prisma.io/docs/orm/v7) | Apache-2.0 |
| `drizzle-orm` | `drizzle-orm`: TypeScript-first SQL ORM and query tooling | [Repo](https://github.com/drizzle-team/drizzle-orm), [docs](https://orm.drizzle.team/docs/overview) | Apache-2.0 |

## Java/JVM backend components (9)

Java/JVM components are not JavaScript/Node packages. Align selected releases,
JDK and Spring/Jakarta/BOM versions with the actual project; inspected build
toolchains/development HEAD do not certify release runtime support.

| Stable library ID | Maven artifact and purpose | Official repository / documentation | License |
| --- | --- | --- | --- |
| `spring-boot` | `org.springframework.boot:spring-boot`: JVM application configuration/framework | [Repo](https://github.com/spring-projects/spring-boot), [docs](https://docs.spring.io/spring-boot/system-requirements.html) | Apache-2.0 |
| `spring-security` | `org.springframework.security:spring-security-core`: Spring authentication and authorization infrastructure | [Repo](https://github.com/spring-projects/spring-security), [docs](https://docs.spring.io/spring-security/reference/) | Apache-2.0 |
| `spring-data-jpa` | `org.springframework.data:spring-data-jpa`: JPA repositories and data-access abstraction | [Repo](https://github.com/spring-projects/spring-data-jpa), [docs](https://docs.spring.io/spring-data/jpa/reference/) | Apache-2.0 |
| `hibernate-validator` | `org.hibernate.validator:hibernate-validator`: Jakarta Bean Validation implementation | [Repo](https://github.com/hibernate/hibernate-validator), [docs](https://hibernate.org/validator/) | Apache-2.0 |
| `flyway` | `org.flywaydb:flyway-core`: Database schema migrations | [Repo](https://github.com/flyway/flyway), [docs](https://documentation.red-gate.com/flyway/) | Apache-2.0 |
| `apache-poi` | `org.apache.poi:poi; org.apache.poi:poi-ooxml`: Office binary/OOXML document read/write | [Repo](https://github.com/apache/poi), [docs](https://poi.apache.org/) | Apache-2.0 |
| `jasperreports` | `net.sf.jasperreports:jasperreports`: Report generation engine | [Repo](https://github.com/Jaspersoft/jasperreports), [docs](https://jasperreports.sourceforge.net/) | LGPL-3.0 (confirm exact selected artifact expression) |
| `quartz` | `org.quartz-scheduler:quartz`: Persistent JVM job scheduling | [Repo](https://github.com/quartz-scheduler/quartz), [docs](https://www.quartz-scheduler.org/) | Apache-2.0 |
| `resilience4j` | `io.github.resilience4j:resilience4j-circuitbreaker`: Circuit breakers/retries/bulkheads and rate limiting | [Repo](https://github.com/resilience4j/resilience4j), [docs](https://resilience4j.readme.io/) | Apache-2.0 |

## Declared-preference reference pair: Next.js and NestJS

When the user/project declares this pair and stack is undecided, assess Next.js
(`nextjs`) with existing NestJS (`nestjs`), then confirm in the project's PRD.
Catalog presence does not make this pair a global plugin default.
Preserve an already approved stack; other users/frameworks remain valid alternatives.
Next handles presentation/rendering/SSR and optional server/BFF adaptation; it can
run backend code. In this selected pair, domain/API business rules and persistence
belong to the Nest-owned boundary. Next adapters call that API rather than copy
domain rules. Auth/session, module and deployment boundaries remain project decisions.
No migration, dependency version or deployment is selected by this preference.

Next.js MIT code does not require Vercel hosting; hosting/provider costs are
separate optional choices. Inspected canary source package is 16.5.0-canary.10,
not an adopted stable release or cross-OS runtime certification.

## Adoption boundaries

Laravel services and a Next.js frontend are separate runtimes joined by explicit
API/auth contracts; a Node backend is a separate choice. Fortify exposes headless
authentication endpoints; SPA session/token, CSRF and authorization design remain
project decisions. Spatie permissions require server-side enforcement, not merely
hidden UI. Activitylog is not immutable audit evidence. Money/wallet helpers do not
provide banking, regulated custody, accounting completeness or reconciliation.
Filament uses Laravel/Livewire administration, not React/Next components.

SDK code license does not make payment services free or guarantee rates/quotas.
Use backend-protected provider credentials and certificates/mTLS where required;
verify webhook authenticity, idempotency, retry/reconciliation and sandbox flows.
NFePHP sped-nfe handles NF-e/NFC-e scope, not general NFS-e coverage; sped-da
renders auxiliary documents, not tax authorization. Fiscal decisions remain with
the existing fiscal/domain owner and official jurisdiction-specific rules.

NFePHP README states LGPLv3 OR MIT and license files contain both. Composer lists
additional GPL identifiers; sped-da's LGPL identifier has a trailing `+`. Preserve
those differing upstream declarations and check chosen files/dependencies, rather
than silently treating the entire fiscal dependency tree as MIT.

BullMQ's selected OSS Node queue route uses Redis and persistent workers, not
browser or Edge-only request execution; PostgreSQL routing is NOT_VALIDATED.
Zod validates shapes, not authorization or tenant isolation. CASL client rules
need server enforcement. Better Auth still needs protected server checks and
project adapter/session design. ExcelJS browser support lacks streaming reader/
writer; PDFKit requires suitable bundling/fonts. Nodemailer is server SMTP with
protected credentials, not a browser mail sender; no email was sent.

Bagisto, Medusa and Vendure are commerce platforms with domain/deployment/migration
impacts, not drop-in UI components or automatically selected ERP architecture.
Medusa root MIT excludes listed Enterprise Materials, including current RBAC/SSO
paths; check ENTERPRISE-LICENSE.md and chosen subtree. Vendure is GPL-3.0-or-later
free core with a plugin exception; commercial VCL is not selected; that exception does not erase Core
modification duties. BullMQ Pro and marketplace add-ons have separate terms.

Framework selection is a project architecture decision. Check release-specific
Node and adapter requirements; neither framework nor ORM presence certifies
Windows10, Linux/macOS, browser or Edge behavior. Fastify inspected main is an
alpha; it is not an adopted stable release. Nest requires appropriate build/module
configuration. Prisma inspected main redirects to prisma/orm and documents v8 RC;
v7 remains on its versioned branch/docs. Generated client/build output, database
driver adapters, connection lifecycle and migration deployment must match the
selected major. Native engine binaries and system dependencies apply to versions/
engine modes that use them; newer Rust-free modes have different requirements.
Do not assume all Prisma versions need the same engine or runtime. Drizzle needs
the selected database driver; TS query types do not replace DB constraints/authz.

Spring Security still needs explicit server access policies; Spring Data JPA
requires a compatible persistence provider/DB/transaction design. Hibernate
Validator checks constraints, not authorization or DB invariants; check Jakarta
versus javax namespace. POI/Jasper reports require chosen formats/templates,
font/data limits and transitive licenses; Jasper LGPL library terms do not cover
all proprietary Jaspersoft products. Quartz needs scheduler lifecycle/storage/
clustering design. Resilience4j retries must respect idempotency and failure budgets.

Use Flyway only when selected against the project's existing migration system;
excluded Liquibase is not an eligible alternative here. Actual migration needs database target,
backup/rollback and approval. Flyway core Apache-2.0 does not cover all paid editions/
drivers. Inspected Liquibase Community5 is FSL-1.1-ALv2, source-available with
competing-commercial restrictions, not currently blanket OSI open source. Its
license has future Apache conversion terms; older4.x and paid Secure are separate
version/product choices. Check the exact selected release/file before adoption.

## Source provenance

Default branch commits observed 2026-10-14; target package versions remain
UNKNOWN until selected and verified. Official pinned package metadata is evidence
of requirements, not an executed compatibility test.

| Library ID | Observed branch | Full commit | Pinned package/license evidence |
| --- | --- | --- | --- |
| `nextjs` | `canary` | `179eba81e0572197a55ac83415d4e91d7cfdea62` | [package](https://github.com/vercel/next.js/blob/179eba81e0572197a55ac83415d4e91d7cfdea62/packages/next/package.json), [license](https://github.com/vercel/next.js/blob/179eba81e0572197a55ac83415d4e91d7cfdea62/license.md) |
| `laravel-fortify` | `1.x` | `f7c3fd787a64ada544353c0423e4589b1626ec75` | [package](https://raw.githubusercontent.com/laravel/fortify/f7c3fd787a64ada544353c0423e4589b1626ec75/composer.json), [license](https://raw.githubusercontent.com/laravel/fortify/f7c3fd787a64ada544353c0423e4589b1626ec75/LICENSE.md) |
| `spatie-permission` | `main` | `6615eefac655efcd652fe394a20cbdf4f72c609f` | [package](https://raw.githubusercontent.com/spatie/laravel-permission/6615eefac655efcd652fe394a20cbdf4f72c609f/composer.json), [license](https://raw.githubusercontent.com/spatie/laravel-permission/6615eefac655efcd652fe394a20cbdf4f72c609f/LICENSE.md) |
| `spatie-activitylog` | `main` | `c37c43b32ea1ff15dc00491c07dafdfb8fd57340` | [package](https://raw.githubusercontent.com/spatie/laravel-activitylog/c37c43b32ea1ff15dc00491c07dafdfb8fd57340/composer.json), [license](https://raw.githubusercontent.com/spatie/laravel-activitylog/c37c43b32ea1ff15dc00491c07dafdfb8fd57340/LICENSE.md) |
| `spatie-medialibrary` | `main` | `1f73cad3497b9b26228ef78b46f900dc49c07286` | [package](https://raw.githubusercontent.com/spatie/laravel-medialibrary/1f73cad3497b9b26228ef78b46f900dc49c07286/composer.json), [license](https://raw.githubusercontent.com/spatie/laravel-medialibrary/1f73cad3497b9b26228ef78b46f900dc49c07286/LICENSE.md) |
| `spatie-query-builder` | `main` | `bdd59bdc0c3c1afcb3f4694c393177afb92fa83b` | [package](https://raw.githubusercontent.com/spatie/laravel-query-builder/bdd59bdc0c3c1afcb3f4694c393177afb92fa83b/composer.json), [license](https://raw.githubusercontent.com/spatie/laravel-query-builder/bdd59bdc0c3c1afcb3f4694c393177afb92fa83b/LICENSE.md) |
| `laravel-excel` | `4.x` | `30f17acbb89bf260173387349722eec2cc817016` | [package](https://raw.githubusercontent.com/SpartnerNL/Laravel-Excel/30f17acbb89bf260173387349722eec2cc817016/composer.json), [license](https://raw.githubusercontent.com/SpartnerNL/Laravel-Excel/30f17acbb89bf260173387349722eec2cc817016/LICENSE) |
| `laravel-dompdf` | `master` | `a7f7e228b91d95f8dde56e1cff236f15713bb0f0` | [package](https://raw.githubusercontent.com/barryvdh/laravel-dompdf/a7f7e228b91d95f8dde56e1cff236f15713bb0f0/composer.json), [license](https://raw.githubusercontent.com/barryvdh/laravel-dompdf/a7f7e228b91d95f8dde56e1cff236f15713bb0f0/LICENSE) |
| `brick-money` | `main` | `93f145c6c9f5b58160e2967088e7e083722e28cc` | [package](https://raw.githubusercontent.com/brick/money/93f145c6c9f5b58160e2967088e7e083722e28cc/composer.json), [license](https://raw.githubusercontent.com/brick/money/93f145c6c9f5b58160e2967088e7e083722e28cc/LICENSE) |
| `laravel-wallet` | `master` | `7587df628b377f11accac4b48bb6eac576e5268b` | [package](https://raw.githubusercontent.com/bavix/laravel-wallet/7587df628b377f11accac4b48bb6eac576e5268b/composer.json), [license](https://raw.githubusercontent.com/bavix/laravel-wallet/7587df628b377f11accac4b48bb6eac576e5268b/LICENSE) |
| `filament` | `4.x` | `0747e62838adcff87b00706ed94a3ed91c46929f` | [package](https://raw.githubusercontent.com/filamentphp/filament/0747e62838adcff87b00706ed94a3ed91c46929f/composer.json), [license](https://raw.githubusercontent.com/filamentphp/filament/0747e62838adcff87b00706ed94a3ed91c46929f/LICENSE.md) |
| `efi-php` | `main` | `b3996b7c9bcd35acba6127e04d07db0dc9778253` | [package](https://raw.githubusercontent.com/efipay/sdk-php-apis-efi/b3996b7c9bcd35acba6127e04d07db0dc9778253/composer.json), [license](https://raw.githubusercontent.com/efipay/sdk-php-apis-efi/b3996b7c9bcd35acba6127e04d07db0dc9778253/LICENSE) |
| `efi-node` | `master` | `d742ee94b76097383c42792494351a68568e23a9` | [package](https://raw.githubusercontent.com/efipay/sdk-node-apis-efi/d742ee94b76097383c42792494351a68568e23a9/package.json), [license](https://raw.githubusercontent.com/efipay/sdk-node-apis-efi/d742ee94b76097383c42792494351a68568e23a9/LICENSE) |
| `mercadopago-php` | `master` | `c5fd9086604c41507b45dfbebab057ba288f19c1` | [package](https://raw.githubusercontent.com/mercadopago/sdk-php/c5fd9086604c41507b45dfbebab057ba288f19c1/composer.json), [license](https://raw.githubusercontent.com/mercadopago/sdk-php/c5fd9086604c41507b45dfbebab057ba288f19c1/LICENSE) |
| `mercadopago-node` | `master` | `bf920b9415ba19986b7ffdbf83a5aa21b589a6e0` | [package](https://raw.githubusercontent.com/mercadopago/sdk-nodejs/bf920b9415ba19986b7ffdbf83a5aa21b589a6e0/package.json), [license](https://raw.githubusercontent.com/mercadopago/sdk-nodejs/bf920b9415ba19986b7ffdbf83a5aa21b589a6e0/LICENSE) |
| `cashier-stripe` | `16.x` | `d8df4daff7a29252ff4ec0298a5364d3bda81ab1` | [package](https://raw.githubusercontent.com/laravel/cashier-stripe/d8df4daff7a29252ff4ec0298a5364d3bda81ab1/composer.json), [license](https://raw.githubusercontent.com/laravel/cashier-stripe/d8df4daff7a29252ff4ec0298a5364d3bda81ab1/LICENSE.md) |
| `nfephp-sped-nfe` | `master` | `346c14d5b7e59ab9aab92e7a77c499a19d462fba` | [package](https://raw.githubusercontent.com/nfephp-org/sped-nfe/346c14d5b7e59ab9aab92e7a77c499a19d462fba/composer.json), [license](https://raw.githubusercontent.com/nfephp-org/sped-nfe/346c14d5b7e59ab9aab92e7a77c499a19d462fba/LICENSE.md) |
| `nfephp-sped-da` | `master` | `308abfe0fe01a3a2c9acfc7b57bf59fcffc77717` | [package](https://raw.githubusercontent.com/nfephp-org/sped-da/308abfe0fe01a3a2c9acfc7b57bf59fcffc77717/composer.json), [license](https://raw.githubusercontent.com/nfephp-org/sped-da/308abfe0fe01a3a2c9acfc7b57bf59fcffc77717/LICENSE) |
| `better-auth` | observed default (branch name UNKNOWN) | `ea85d133d640233c1564417f3bad611d99356bb9` | [README](https://github.com/better-auth/better-auth/blob/ea85d133d640233c1564417f3bad611d99356bb9/README.md), [license](https://raw.githubusercontent.com/better-auth/better-auth/ea85d133d640233c1564417f3bad611d99356bb9/LICENSE.md) |
| `casl` | observed default (branch name UNKNOWN) | `9ed32616975a1725f0c681b6380605843cabb914` | [README](https://github.com/stalniy/casl/blob/9ed32616975a1725f0c681b6380605843cabb914/README.md), [license](https://raw.githubusercontent.com/stalniy/casl/9ed32616975a1725f0c681b6380605843cabb914/LICENSE) |
| `bullmq` | observed default (branch name UNKNOWN) | `03655d4b8aa77682df93dd70bd20c60c5769c894` | [README](https://github.com/taskforcesh/bullmq/blob/03655d4b8aa77682df93dd70bd20c60c5769c894/README.md), [license](https://raw.githubusercontent.com/taskforcesh/bullmq/03655d4b8aa77682df93dd70bd20c60c5769c894/LICENSE) |
| `zod` | observed default (branch name UNKNOWN) | `680d19f7d1e042e55934209caeb79bc843b94f44` | [README](https://github.com/colinhacks/zod/blob/680d19f7d1e042e55934209caeb79bc843b94f44/README.md), [license](https://raw.githubusercontent.com/colinhacks/zod/680d19f7d1e042e55934209caeb79bc843b94f44/LICENSE) |
| `exceljs` | observed default (branch name UNKNOWN) | `5bed18b45e824f409b08456b59b87430ded023ab` | [README](https://github.com/exceljs/exceljs/blob/5bed18b45e824f409b08456b59b87430ded023ab/README.md), [license](https://raw.githubusercontent.com/exceljs/exceljs/5bed18b45e824f409b08456b59b87430ded023ab/LICENSE) |
| `pdfkit` | observed default (branch name UNKNOWN) | `e2fafd2b22af778a22cf9c734e9a63e753e79025` | [README](https://github.com/foliojs/pdfkit/blob/e2fafd2b22af778a22cf9c734e9a63e753e79025/README.md), [license](https://raw.githubusercontent.com/foliojs/pdfkit/e2fafd2b22af778a22cf9c734e9a63e753e79025/LICENSE) |
| `nodemailer` | observed default (branch name UNKNOWN) | `c8671c47559be03614230904cb9df559a8a12130` | [README](https://github.com/nodemailer/nodemailer/blob/c8671c47559be03614230904cb9df559a8a12130/README.md), [license](https://raw.githubusercontent.com/nodemailer/nodemailer/c8671c47559be03614230904cb9df559a8a12130/LICENSE) |
| `bagisto` | observed default (branch name UNKNOWN) | `e3ba5b00b3df35390175b77b59826fa24f8183c4` | [README](https://github.com/bagisto/bagisto/blob/e3ba5b00b3df35390175b77b59826fa24f8183c4/README.md), [license](https://raw.githubusercontent.com/bagisto/bagisto/e3ba5b00b3df35390175b77b59826fa24f8183c4/LICENSE) |
| `medusa` | observed default (branch name UNKNOWN) | `d37c79548bad6e9ef2ad00cfa63bdcf4be123ba4` | [README](https://github.com/medusajs/medusa/blob/d37c79548bad6e9ef2ad00cfa63bdcf4be123ba4/README.md), [license](https://raw.githubusercontent.com/medusajs/medusa/d37c79548bad6e9ef2ad00cfa63bdcf4be123ba4/LICENSE) |
| `vendure` | observed default (branch name UNKNOWN) | `983ae280ace89588efdbf85dc95f2a16d3fb3d73` | [README](https://github.com/vendurehq/vendure/blob/983ae280ace89588efdbf85dc95f2a16d3fb3d73/README.md), [license](https://raw.githubusercontent.com/vendurehq/vendure/983ae280ace89588efdbf85dc95f2a16d3fb3d73/LICENSE.md) |

[Medusa Enterprise terms](https://github.com/medusajs/medusa/blob/d37c79548bad6e9ef2ad00cfa63bdcf4be123ba4/ENTERPRISE-LICENSE.md), [Vendure plugin exception](https://github.com/vendurehq/vendure/blob/983ae280ace89588efdbf85dc95f2a16d3fb3d73/license/plugin-exception.txt).

| Library ID | Observed branch | Full commit | Pinned source/license evidence |
| --- | --- | --- | --- |
| `express` | `master` | `a419aa7350389a275ab45fde2e849ed1f02449ef` | [README](https://github.com/expressjs/express/blob/a419aa7350389a275ab45fde2e849ed1f02449ef/Readme.md), [license](https://raw.githubusercontent.com/expressjs/express/a419aa7350389a275ab45fde2e849ed1f02449ef/LICENSE) |
| `fastify` | `main` | `e222f53aa267080b349eacdeaff03ea9a061e8c7` | [README](https://github.com/fastify/fastify/blob/e222f53aa267080b349eacdeaff03ea9a061e8c7/README.md), [license](https://raw.githubusercontent.com/fastify/fastify/e222f53aa267080b349eacdeaff03ea9a061e8c7/LICENSE) |
| `nestjs` | `master` | `fa152aff7ecdc6995f139a3a579f09c63b6aba22` | [README](https://github.com/nestjs/nest/blob/fa152aff7ecdc6995f139a3a579f09c63b6aba22/Readme.md), [license](https://raw.githubusercontent.com/nestjs/nest/fa152aff7ecdc6995f139a3a579f09c63b6aba22/LICENSE) |
| `prisma` | `main` | `9d489d5d24b82d1a00bd0e2bca06b70081bef803` | [README](https://github.com/prisma/prisma/blob/9d489d5d24b82d1a00bd0e2bca06b70081bef803/README.md), [license](https://raw.githubusercontent.com/prisma/prisma/9d489d5d24b82d1a00bd0e2bca06b70081bef803/LICENSE) |
| `drizzle-orm` | `main` | `eab8bedbb65d5429c54e612ddbd88aa23091d398` | [README](https://github.com/drizzle-team/drizzle-orm/blob/eab8bedbb65d5429c54e612ddbd88aa23091d398/README.md), [license](https://raw.githubusercontent.com/drizzle-team/drizzle-orm/eab8bedbb65d5429c54e612ddbd88aa23091d398/LICENSE) |

[Prisma versioned system requirements](https://docs.prisma.io/docs/orm/reference/system-requirements), [Prisma engine/version differences](https://docs.prisma.io/docs/orm/v6/more/internals/engines), [Fastify LTS policy](https://github.com/fastify/fastify/blob/e222f53aa267080b349eacdeaff03ea9a061e8c7/docs/Reference/LTS.md).

| Library ID | Observed source | Full commit | Pinned source/license evidence |
| --- | --- | --- | --- |
| `spring-boot` | default HEAD (branch name UNKNOWN) | `c6be2d61c837a82eec40de9141dc4f3100d1c79c` | [source](https://raw.githubusercontent.com/spring-projects/spring-boot/c6be2d61c837a82eec40de9141dc4f3100d1c79c/README.adoc), [license](https://raw.githubusercontent.com/spring-projects/spring-boot/c6be2d61c837a82eec40de9141dc4f3100d1c79c/LICENSE.txt) |
| `spring-security` | default HEAD (branch name UNKNOWN) | `ab9c14c12f9503817b08c3253572a51dfbe2f09c` | [source](https://raw.githubusercontent.com/spring-projects/spring-security/ab9c14c12f9503817b08c3253572a51dfbe2f09c/README.adoc), [license](https://raw.githubusercontent.com/spring-projects/spring-security/ab9c14c12f9503817b08c3253572a51dfbe2f09c/LICENSE.txt) |
| `spring-data-jpa` | default HEAD (branch name UNKNOWN) | `27bee87c69b9a0f63a1c7379ba59db6c12273ea0` | [source](https://raw.githubusercontent.com/spring-projects/spring-data-jpa/27bee87c69b9a0f63a1c7379ba59db6c12273ea0/README.adoc), [license](https://raw.githubusercontent.com/spring-projects/spring-data-jpa/27bee87c69b9a0f63a1c7379ba59db6c12273ea0/LICENSE.txt) |
| `hibernate-validator` | default HEAD (branch name UNKNOWN) | `6e644cd2c447d7ad5aebe76d5e92035ce5613dee` | [source](https://raw.githubusercontent.com/hibernate/hibernate-validator/6e644cd2c447d7ad5aebe76d5e92035ce5613dee/README.md), [license](https://raw.githubusercontent.com/hibernate/hibernate-validator/6e644cd2c447d7ad5aebe76d5e92035ce5613dee/license.txt) |
| `flyway` | default HEAD (branch name UNKNOWN) | `b4251cdbec1a6c8ec6b15c9f3f99976d7b8ef251` | [source](https://raw.githubusercontent.com/flyway/flyway/b4251cdbec1a6c8ec6b15c9f3f99976d7b8ef251/README.md), [license](https://raw.githubusercontent.com/flyway/flyway/b4251cdbec1a6c8ec6b15c9f3f99976d7b8ef251/LICENSE.txt) |
| `apache-poi` | default HEAD (branch name UNKNOWN) | `18d4128d956f9436bfe06c10cfdd457fca6a61de` | [source](https://raw.githubusercontent.com/apache/poi/18d4128d956f9436bfe06c10cfdd457fca6a61de/README.md), [license](https://poi.apache.org/legal.html) |
| `jasperreports` | default HEAD (branch name UNKNOWN) | `9e4760d73647e9c11bbbddbcd06624a0255703eb` | [source](https://raw.githubusercontent.com/Jaspersoft/jasperreports/9e4760d73647e9c11bbbddbcd06624a0255703eb/README.md), [license](https://raw.githubusercontent.com/Jaspersoft/jasperreports/9e4760d73647e9c11bbbddbcd06624a0255703eb/LICENSE) |
| `quartz` | default HEAD (branch name UNKNOWN) | `741ccc3cff96a32e4ab07d69624eaaa534624245` | [source](https://raw.githubusercontent.com/quartz-scheduler/quartz/741ccc3cff96a32e4ab07d69624eaaa534624245/build.gradle), [license](https://raw.githubusercontent.com/quartz-scheduler/quartz/741ccc3cff96a32e4ab07d69624eaaa534624245/LICENSE.txt) |
| `resilience4j` | default HEAD (branch name UNKNOWN) | `b7c0069802e373ed72dff0b817c270fbb6e966ba` | [source](https://raw.githubusercontent.com/resilience4j/resilience4j/b7c0069802e373ed72dff0b817c270fbb6e966ba/README.adoc), [license](https://raw.githubusercontent.com/resilience4j/resilience4j/b7c0069802e373ed72dff0b817c270fbb6e966ba/LICENSE.txt) |

Apache POI Apache-2.0 was verified from its official legal page. The pinned
repository root license path is UNKNOWN; the legal-page link is not an attestation
of a commit-pinned license file. Check chosen release license/NOTICE on adoption.
