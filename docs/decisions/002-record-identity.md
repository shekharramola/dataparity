# ADR-002: Record Identity

## Status

Accepted

## Context

DataParity compares recurring versions of the same logical dataset. To
determine whether a record is added, removed, unchanged, or modified, the
system must reliably identify the same logical record across dataset versions.

A record cannot be matched reliably using its physical row position because
rows may be reordered between versions.

Different datasets may use different business identifiers. Some datasets may
require more than one column to uniquely identify a record.

## Decision

DataParity will use a user-configured record identity to match records across
dataset versions.

During dataset configuration, the user must select one or more columns that
together identify a record.

A single selected column represents a simple record key.

Multiple selected columns represent a composite record key. Composite keys are
treated as an ordered set of configured fields whose combined normalized values
identify a record.

Record identity must be established before a dataset version can be compared
against an approved baseline.

DataParity will validate the configured record identity before comparison.
The configured identity must be present in the dataset and must provide
sufficient uniqueness for reliable record matching.

Record identity fields are normalized according to the applicable comparison
rules before matching.

Changes to configured record-identity columns receive elevated severity because
they can affect record matching and the correctness of subsequent comparisons.

Changing the record-identity configuration is treated as a dataset
configuration change and must not silently reinterpret historical comparisons.

## Rationale

Stable business identity is more reliable than row position for recurring
dataset comparison.

Supporting composite keys allows DataParity to handle datasets where no
single column uniquely identifies a record.

Requiring explicit configuration avoids silently guessing a business identity
that could produce incorrect comparison results.

## Consequences

### Positive

- Records can be matched correctly even when row ordering changes.
- Composite-key datasets are supported.
- Comparison results become deterministic and explainable.
- Reviewers can understand which fields determine record identity.
- Historical comparisons remain tied to the identity configuration under which
  they were performed.

### Negative

- Users must configure record identity when creating a dataset.
- Poorly chosen or unstable keys can produce incorrect comparisons.
- DataParity must validate key uniqueness and handle duplicate identities.
- Changing identity configuration requires explicit handling.

## Alternatives Considered

### Row Position

Rejected because row ordering can change between dataset versions and does not
represent business identity.

### Automatic Key Inference

Rejected as the primary mechanism because DataParity cannot reliably determine
the intended business identity from arbitrary datasets without risking incorrect
record matching.

Automatic inference may be considered as a future recommendation that the
user explicitly confirms.

### Hashing Entire Records

Rejected as the primary identity mechanism because a record hash detects
content equality but does not provide stable identity when field values change.