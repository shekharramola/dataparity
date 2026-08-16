# ADR-004: Time-Bound Licensing and Offline Validation

## Status

Accepted

## Context

DataParity is intended to be commercially distributed as a local-first
application.

The product will use time-bound licenses rather than requiring a recurring
subscription for continuous application access.

Customers may purchase different license terms, including:

- 1 month
- 3 months
- 6 months
- 12 months

The application must remain usable offline during the valid license period.
Core customer dataset processing must not depend on continuous communication
with a licensing service.

At the same time, the licensing system must prevent simple modification of
license expiration dates or other entitlement information.

## Decision

DataParity will use digitally signed, time-bound license entitlements.

A license will contain information such as:

- License identifier
- Product identifier
- Issued-at timestamp
- Expiration timestamp
- License term
- Entitlement information
- Signature

The licensing service will issue and manage licenses. A centralized licensing
service may use PostgreSQL for license, activation, renewal, and entitlement
records.

The customer's DataParity installation will contain the public key required
to verify license signatures. The private signing key will remain exclusively
under the control of the licensing service.

After activation, DataParity will store the signed license entitlement locally
and validate the signature and expiration status locally.

Normal dataset ingestion, comparison, analysis, review, and export will not
require communication with the licensing service.

Online communication may be required for initial activation, renewal, device
activation, or other explicitly defined licensing operations.

## License Expiration

The signed license contains an expiration timestamp.

DataParity can determine whether the license is expired using the local system
clock without contacting the licensing service.

License expiration must not affect the integrity or availability of previously
approved customer datasets. Expiration affects licensing entitlement only.

Handling of significant system-clock manipulation, offline grace periods, and
device transfer limits will be defined as part of the licensing
implementation.

## License Security

License data must be cryptographically signed so that customers cannot modify
entitlement information without invalidating the signature.

The application must never contain the private signing key.

Local license credentials should be stored using the platform's secure
credential storage facilities where appropriate.

The licensing service must not require access to customer dataset contents.

## Rationale

Time-bound licensing provides a straightforward commercial model while
preserving the local-first nature of the application.

Digital signatures allow licenses to be validated offline while protecting
against simple modification of expiration dates or entitlements.

Separating licensing infrastructure from dataset processing ensures that
commercial infrastructure does not become a dependency for customer data
processing.

Using PostgreSQL for the centralized licensing service is appropriate because
licensing represents a shared transactional workload involving multiple
customers, licenses, activations, and renewals.

## Consequences

### Positive

- DataParity can operate offline during a valid license period.
- Customer datasets remain outside the licensing infrastructure.
- License terms can be offered in multiple durations.
- License integrity can be verified cryptographically.
- Licensing infrastructure can evolve independently from the local processing
  engine.
- PostgreSQL can be used meaningfully in a centralized service without
  requiring it on the customer's machine.

### Negative

- Initial activation or renewal may require internet connectivity.
- System-clock manipulation requires additional protection if strong license
  enforcement is required.
- A licensing service must be operated for commercial distribution.
- License recovery and device-transfer workflows must be designed.

## Alternatives Considered

### Continuous Online License Verification

Rejected because requiring continuous connectivity would conflict with the
local-first and offline usability goals.

### Unsigned Local License File

Rejected because users could modify expiration dates or entitlements without
cryptographic verification.

### Perpetual License With No Expiration

Rejected because the product is intended to support selectable time-bound
commercial terms.

### Subscription-Only Enforcement

Rejected because the MVP licensing model is based on explicit license terms
rather than requiring continuous recurring billing and network connectivity.