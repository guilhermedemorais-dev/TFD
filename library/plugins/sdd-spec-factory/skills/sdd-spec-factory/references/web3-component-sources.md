# Web3 component sources

Source-only discovery catalog: 11 requested identities, 10 eligible free-code/toolchain
sources and 1 excluded identity. Checked 2026-10-14. Reuse project-native code first,
then matching candidates, then targeted official-source research for gaps. Keep
the every-PRD/spec metadata consultation/selection/native-reuse or justified N/A
record and existing project source-ID handoff. Only chosen necessary bodies are
REQUIRED. Select an edition/item usable without purchasing a license; unknown
terms/costs and paid assets are ineligible until verified.

Source pins identify inspected revisions, not selected releases or production
compatibility. Library code cost differs from hosted RPC/account/API/gas fees.
No installation, wallet/account, key handling, RPC, signing, transaction, funds,
contract deployment or paid service is authorized. No runtime/OS/security audit
was performed. Skills remain OS-neutral. Hardhat/Foundry below are development
toolchains discovered as sources, not installed libraries, OS tool routes or MCPs.

## Eligible PHP libraries and development toolchain sources (4)

| Stable ID | Package/tool identity and purpose | Official repo/docs | License scope |
| --- | --- | --- | --- |
| `web3-php` | `web3p/web3.php`: PHP Ethereum JSON-RPC client; distinct from similarly named forks | [repo](https://github.com/web3p/web3.php), [docs](https://github.com/web3p/web3.php#readme) | MIT |
| `ethereum-tx-php` | `web3p/ethereum-tx`: PHP Ethereum transaction representation/signing helpers | [repo](https://github.com/web3p/ethereum-tx), [docs](https://github.com/web3p/ethereum-tx#readme) | MIT |
| `hardhat` | `hardhat`: JavaScript/TypeScript Ethereum development toolchain | [repo](https://github.com/NomicFoundation/hardhat), [docs](https://hardhat.org/docs) | MIT |
| `foundry` | `forge/cast/anvil/chisel`: Rust Ethereum development and testing toolchain | [repo](https://github.com/foundry-rs/foundry), [docs](https://getfoundry.sh/) | MIT OR Apache-2.0 |

## Eligible JS/TypeScript and Solidity source candidates (6)

| Stable ID | Package identity and purpose | Official repo/docs | License scope |
| --- | --- | --- | --- |
| `viem` | `viem`: Typed EVM clients/ABI and RPC abstractions | [repo](https://github.com/wevm/viem), [docs](https://viem.sh/) | MIT |
| `ethers` | `ethers`: Ethereum providers/contracts/signers library | [repo](https://github.com/ethers-io/ethers.js), [docs](https://docs.ethers.org/v6/) | MIT |
| `wagmi` | `wagmi`: React EVM wallet hooks and connection state | [repo](https://github.com/wevm/wagmi), [docs](https://wagmi.sh/react/getting-started) | MIT |
| `openzeppelin-contracts` | `@openzeppelin/contracts`: Solidity EVM contract modules | [repo](https://github.com/OpenZeppelin/openzeppelin-contracts), [docs](https://docs.openzeppelin.com/contracts/5.x) | MIT |
| `thirdweb` | `thirdweb`: TypeScript SDK source only; hosted services excluded | [repo](https://github.com/thirdweb-dev/js), [docs](https://portal.thirdweb.com/typescript/v5/client) | Apache-2.0 |
| `solana-kit` | `@solana/kit`: Modern Solana JS/TS SDK, distinct from legacy web3.js 1.x | [repo](https://github.com/anza-xyz/kit), [docs](https://www.solanakit.com/) | MIT |

## Excluded identity, retained for traceability (1)

`reown-appkit`, `@reown/appkit` ([repo](https://github.com/reown-com/appkit), [docs](https://docs.reown.com/appkit/overview)), source `8f9f39f1dfe0a21bb619dd9a33b6d7500523298b`: EXCLUDED from active free candidates.
[Pinned Community license](https://raw.githubusercontent.com/reown-com/appkit/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/LICENSE.md) is custom/restrictive, not MIT. It requires
proprietary Reown Network connection and modification-rights conditions; the
inspected terms trigger commercial licensing above either 2.5 million monthly RPC
requests or 500 monthly active users and reserve changing triggers. These are
source-specific terms, not a guaranteed permanent free tier. No claim all uses
are paid: excluded by default until project terms/costs are reviewed separately.
Reading public documentation does not connect any wallet/network.

## Adoption boundaries

web3.php here identifies web3p/web3.php, not similarly named repositories/forks.
PHP JSON-RPC access needs a selected chain/node/provider and server boundary;
transaction helpers do not supply secure key custody, nonce/gas policy, network
selection or authorization. Review transaction formats and chosen package release.
Never place signing secrets in client code or source records. No signing was done.

Hardhat and Foundry support contract development/testing; choosing a source does
not install compilers, dependencies or engines. Check selected release Node/Rust,
compiler, plugin/subcrate license and runtime requirements. Local test tooling
and upstream popularity do not prove contract security or cross-OS support.

Viem and Ethers are alternative EVM client choices, not mandatory dual installs.
Wagmi's `wagmi` package is React-specific; other-framework/core variants are
separate selections. UI connection state does not implement server authorization;
check SSR hydration, providers/connectors and their separate service terms.
OpenZeppelin is Solidity code, not app authentication. Select exact contracts/
compiler/upgrades: a contract's pragma and reputation do not certify all modules
or the financial security of a project. No compile/audit/deploy was performed.

Thirdweb Apache-2.0 eligibility covers SDK source only; hosted RPC/IPFS/wallet/
bundler/paymaster/indexer paid or usage services are EXCLUDED_NOT_APPROVED.
Official client setup needs clientId or secretKey, not an unlimited service grant;
no account/client ID/key was created. Protect server secrets, never browser-bundle
secretKey. Solana Kit uses `@solana/kit` from anza-xyz/kit; legacy @solana/web3.js 1.x
is a separate API/maintenance line, not an automatic compatible replacement.

Hardhat MIT scope is supported by its pinned
[hardhat package metadata](https://github.com/NomicFoundation/hardhat/blob/a27d41f3118f1de0eff9f4cf04de540b69857b9d/packages/hardhat/package.json).
Repository root terms defer to individual package license files; do not assume
all plugins/packages share that package license. Foundry workspace declares
MIT OR Apache-2.0; verify chosen crate/dependency terms separately.

## Source provenance

All entries CANDIDATE_NOT_INSTALLED, runtime/security NOT_VALIDATED. Package version
UNKNOWN until project selection. Checked 2026-10-14; keep exact revision/license
references and verify selected subtree/release again on adoption.

| Stable ID | Observed branch | Full commit | Pinned source/license evidence |
| --- | --- | --- | --- |
| `web3-php` | `master` | `716082dd45709e3950c9dddfd4e39d2fe1fb300b` | [source](https://raw.githubusercontent.com/web3p/web3.php/716082dd45709e3950c9dddfd4e39d2fe1fb300b/README.md), [license](https://raw.githubusercontent.com/web3p/web3.php/716082dd45709e3950c9dddfd4e39d2fe1fb300b/LICENSE) |
| `ethereum-tx-php` | `master` | `74ee021d5c8d8c15ab3ab8c0e2c7c230d44c18d8` | [source](https://raw.githubusercontent.com/web3p/ethereum-tx/74ee021d5c8d8c15ab3ab8c0e2c7c230d44c18d8/README.md), [license](https://raw.githubusercontent.com/web3p/ethereum-tx/74ee021d5c8d8c15ab3ab8c0e2c7c230d44c18d8/LICENSE) |
| `hardhat` | `main` | `a27d41f3118f1de0eff9f4cf04de540b69857b9d` | [source](https://raw.githubusercontent.com/NomicFoundation/hardhat/a27d41f3118f1de0eff9f4cf04de540b69857b9d/README.md), [license](https://raw.githubusercontent.com/NomicFoundation/hardhat/a27d41f3118f1de0eff9f4cf04de540b69857b9d/LICENSE) |
| `foundry` | `master` | `f14e39d2a14d2ba9e9132b0aa7e10a3932a054fc` | [source](https://raw.githubusercontent.com/foundry-rs/foundry/f14e39d2a14d2ba9e9132b0aa7e10a3932a054fc/README.md), [license](https://raw.githubusercontent.com/foundry-rs/foundry/f14e39d2a14d2ba9e9132b0aa7e10a3932a054fc/LICENSE-MIT), [license](https://raw.githubusercontent.com/foundry-rs/foundry/f14e39d2a14d2ba9e9132b0aa7e10a3932a054fc/LICENSE-APACHE) |

| Stable eligible ID | Observed source | Full commit | Pinned source/license evidence |
| --- | --- | --- | --- |
| `viem` | default HEAD (branch name UNKNOWN) | `26608ff3b4bd4e74b26d750729a8a75f69a32913` | [source](https://raw.githubusercontent.com/wevm/viem/26608ff3b4bd4e74b26d750729a8a75f69a32913/src/README.md), [license](https://raw.githubusercontent.com/wevm/viem/26608ff3b4bd4e74b26d750729a8a75f69a32913/src/LICENSE) |
| `ethers` | default HEAD (branch name UNKNOWN) | `3ea4c226dd0b3a074abf90748de9d11192027f4f` | [source](https://raw.githubusercontent.com/ethers-io/ethers.js/3ea4c226dd0b3a074abf90748de9d11192027f4f/README.md), [license](https://raw.githubusercontent.com/ethers-io/ethers.js/3ea4c226dd0b3a074abf90748de9d11192027f4f/LICENSE.md) |
| `wagmi` | default HEAD (branch name UNKNOWN) | `c458d201b0218a9e371de9fdd9a35b6b475fb1b2` | [source](https://wagmi.sh/react/getting-started), [license](https://raw.githubusercontent.com/wevm/wagmi/c458d201b0218a9e371de9fdd9a35b6b475fb1b2/LICENSE) |
| `openzeppelin-contracts` | default HEAD (branch name UNKNOWN) | `97430aa29ac10a70ee0c18f2a905c4925363b58f` | [source](https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/97430aa29ac10a70ee0c18f2a905c4925363b58f/README.md), [license](https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/97430aa29ac10a70ee0c18f2a905c4925363b58f/LICENSE) |
| `thirdweb` | default HEAD (branch name UNKNOWN) | `22741c96f9dcb59d5e18ab5af4e858124938bcae` | [source](https://raw.githubusercontent.com/thirdweb-dev/js/22741c96f9dcb59d5e18ab5af4e858124938bcae/README.md), [license](https://raw.githubusercontent.com/thirdweb-dev/js/22741c96f9dcb59d5e18ab5af4e858124938bcae/LICENSE) |
| `solana-kit` | default HEAD (branch name UNKNOWN) | `e543031b33daa77468befdb10f1c547a19703554` | [source](https://raw.githubusercontent.com/anza-xyz/kit/e543031b33daa77468befdb10f1c547a19703554/README.md), [license](https://raw.githubusercontent.com/anza-xyz/kit/e543031b33daa77468befdb10f1c547a19703554/LICENSE) |
