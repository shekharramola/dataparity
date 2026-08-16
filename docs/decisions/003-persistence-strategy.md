# ADR-003: Persistence Strategy

## Status

Accepted

## Context

DataParity has two distinct persistence requirements.

First, the application needs transactional storage for dataset metadata,
configuration, version state, validation rules, review decisions, findings,
and audit history.

Second, DataParity needs to process and analyze potentially large tabular
datasets efficiently.

The MVP is a local-first, self-contained application and must not require users
to install or operate a database server.

Future hosted or enterprise deployments may require centralized transactional
persistence and multi-user access.

## Decision

DataParity will separate transactional application persistence from analytical
dataset processing.

### Local MVP

SQLite will be used for transactional application state and metadata,
including:

- Datasets
- Dataset versions
- Record-identity configuration
- Validation rules
- Review decisions
- Findings
- Audit history
- Application configuration

The analytical processing layer will use an appropriate local analytical
technology for structured tabular dataset processing.

DuckDB, Polars, pandas, or another suitable implementation may be evaluated
against representative DataParity workloads before the analytical storage
technology is finalized.

The analytical implementation must remain behind the processing-engine
boundary so that the choice of analytical technology does not leak into the
domain model.

The local filesystem will be used for:

- Original source files
- Repaired or normalized artifacts where retention is required
- Generated exports
- Other file-based application artifacts

The application will not require a separately installed PostgreSQL server for
the local MVP.

### Hosted and Enterprise Deployment

PostgreSQL will be supported as a centralized transactional persistence
implementation for future hosted or enterprise deployments.

The application and domain layers will interact with persistence through
defined interfaces rather than depending directly on SQLite or PostgreSQL.

PostgreSQL may also be used during development and integration testing to
validate the production-oriented persistence implementation.

## Rationale

SQLite is appropriate for the local MVP because it provides transactional
persistence without requiring a database server or network connection.

DataParity's core processing involves comparison, filtering, aggregation, and
analysis of tabular data. The analytical implementation should therefore be
selected based on representative workload benchmarks, memory characteristics,
implementation complexity, and support for the required comparison operations.

The filesystem is appropriate for source and generated file artifacts because
these artifacts are naturally file-based and may be substantially larger than
application metadata.

PostgreSQL is appropriate for future hosted and enterprise deployments where
centralized access, concurrent users, stronger operational controls, and
server-based database capabilities become important.

Separating persistence responsibilities prevents the transactional metadata
store from becoming tightly coupled to the analytical processing engine.

## Consequences

### Positive

- The MVP remains self-contained and plug-and-play.
- Users do not need to install or manage PostgreSQL.
- Analytical processing can use a database engine suited to tabular workloads.
- Transactional application state remains separate from dataset analysis.
- The persistence layer can evolve independently of the domain and processing
  engine.
- PostgreSQL experience and integration can be developed without making it a
  mandatory local dependency.
- Future hosted deployments have a clear migration path.

### Negative

- The MVP may use separate technologies for transactional metadata and
  analytical processing.
- The application must define clear boundaries between metadata persistence
  and analytical processing.
- Multiple persistence implementations require additional testing.
- Dataset lifecycle and consistency across transactional metadata, analytical
  processing, and the filesystem must be designed carefully.

## Alternatives Considered

### PostgreSQL for the Local MVP

Rejected because requiring a PostgreSQL server would conflict with the
self-contained and plug-and-play requirements of the MVP.

### SQLite for All Workloads

Rejected because SQLite is primarily being used for transactional application
state and is not the preferred analytical engine for potentially large
tabular comparison workloads.

### Single Database for All Workloads

Rejected for the MVP because transactional application state and analytical
dataset processing have different workload characteristics.

The analytical implementation will be selected after evaluating representative
DataParity workloads.

### Single Database for All Workloads

Rejected for the MVP because the transactional and analytical workloads have
different characteristics and requirements.