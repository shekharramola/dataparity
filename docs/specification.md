# DataParity Specification

## 1. Product Overview

DataParity analyzes incoming recurring structured datasets against previously approved data, producing a detailed analysis of schema, record, and field-level differences, identifying data-quality issues and potentially risky changes, and providing a review workflow for users to investigate, approve, or reject changes before the updated data is accepted for downstream use.

## 2. Primary User

The primary user is a data or operations professional responsible for receiving, reviewing, and approving recurring datasets from external suppliers, partners, or internal data sources. DataParity is designed to let non-developers understand dataset changes, investigate potential data-quality or downstream risks, and approve or reject changes before the data is accepted for downstream use.

## 3. Core Workflow

DataParity manages recurring structured data as logical datasets composed of multiple versions.

A dataset begins when a user creates a dataset and imports an initial file. The initial file is validated and presented for review before it can become the approved baseline.

Once a baseline has been approved, subsequent incoming files are treated as new dataset versions and analyzed against the latest approved version.

Each incoming version passes through validation, comparison, change analysis, and review. The reviewer can approve or reject the version.

An approved version becomes the new baseline for subsequent comparisons. A rejected version does not replace the existing baseline and remains available for historical inspection and audit purposes.


## 4. Dataset & Versioning

DataParity operates on versioned datasets. The first uploaded dataset becomes the initial baseline after explicit approval. Each subsequent incoming dataset is evaluated against the latest approved version.

An incoming dataset remains under review until the reviewer approves or rejects the proposed changes. An approved version becomes the new baseline, while a rejected version does not alter the currently approved dataset.

DataParity retains the history of dataset versions and their associated comparison and review outcomes.

A dataset represents a logical collection of recurring structured data rather than an individual source file.

Each dataset contains one or more versions. A version represents a specific submitted state of the dataset and retains its relationship to the source file, processing results, analysis findings, and review decision.

A dataset can have only one active approved baseline at a time.

Dataset versions can have the following review states:

- `UNDER_REVIEW`
- `APPROVED`
- `REJECTED`

The initial dataset version must be explicitly approved before becoming the active baseline.

A rejected version does not modify the active baseline and is retained for historical inspection and auditability.

### 4.1 No-Change Versions

After validation and normalization, DataParity compares the incoming version against the active approved baseline.

If no meaningful data or schema differences are detected, the version is classified as `NO_CHANGES` and does not require manual review.

The submitted version remains recorded for historical purposes, but the active baseline is unchanged.

DataParity distinguishes source-file identity from logical dataset equivalence. File metadata or binary differences alone must not necessarily be treated as meaningful dataset changes.


## 5. File Ingestion

DataParity MVP supports CSV and XLSX files.

The ingestion layer is responsible for parsing supported files, detecting structural problems, performing only deterministic and safely verifiable repairs, and producing a normalized internal representation for subsequent analysis.

The original source file is never modified.

### 5.1 Recoverable File Issues

DataParity may automatically repair issues when the repair is deterministic and does not alter the semantic meaning of the data. All automatic repairs must be recorded as part of the processing result.

Examples include common encoding markers, line-ending normalization, and other safely recoverable formatting issues.

If a file cannot be safely recovered, processing stops and the user receives an actionable error.

### 5.2 Empty Files

Files containing no usable records are rejected and are not processed as dataset versions.

### 5.3 Duplicate Columns

Duplicate column names are detected during ingestion.

If duplicate columns contain identical values and can be deterministically reduced without loss of information, DataParity may propose or perform the reduction and record the repair.

If duplicate columns contain conflicting values, the file is rejected for manual correction.

### 5.4 Excel Worksheets

For XLSX files containing multiple worksheets, the user must select the worksheet to analyze. DataParity does not automatically merge multiple worksheets in the MVP.

### 5.5 Unsupported Formats

Files other than the supported CSV and XLSX formats are rejected with a clear indication that the format is not currently supported.

Additional file formats may be introduced through future ingestion adapters without changing the core dataset comparison model.

### 5.6 Dataset Scale

DataParity MVP does not impose an arbitrary hard limit on dataset file size.

The application must process datasets within the resource constraints of the
user's machine and should avoid unnecessary full in-memory loading when the
selected processing strategy supports incremental or out-of-core processing.

If a dataset cannot be safely processed with the available local resources,
DataParity must fail gracefully and provide an actionable explanation rather
than exhausting system resources or producing incomplete analysis.


## 6. Record Identity

Each dataset must have a stable record identity that allows DataParity to match records between dataset versions. During dataset configuration, the user can select one or more columns as the record key. DataParity uses the configured key to identify added, removed, unchanged, and modified records across versions.

Composite keys are supported when a single column is insufficient to uniquely identify a record.


## 7. Schema Handling

DataParity compares the schema of each incoming dataset against the latest approved version. Schema differences, including added or removed columns, are identified and presented as reviewable changes.

Schema changes are not automatically accepted or rejected. DataParity flags the change and provides sufficient context for the reviewer to determine whether the updated schema should be approved.

The reviewer remains the final authority for accepting or rejecting schema changes.

### 7.1 Data Type Changes

DataParity detects changes to the inferred or configured data type of existing columns. Type changes are classified according to their potential compatibility impact and presented to the reviewer with the previous type, incoming type, affected records, and potential downstream implications.

Potentially breaking type changes receive a higher severity classification but are not automatically rejected. The reviewer remains responsible for the final decision.

Changes affecting configured record-identity columns receive elevated severity because they can affect record matching and the correctness of subsequent change analysis.


## 8. Record Comparison

DataParity compares records using the configured record identity and classifies each record as one of four fundamental states: added, removed, unchanged, or modified.

Modified records are analyzed further at the field level to identify exactly which values changed between the approved and incoming versions.

Record-level and field-level changes are retained as structured analysis results so that reviewers can understand not only what changed, but also the nature and extent of each change.

### 8.1 Normalization and Comparison

DataParity normalizes values according to their configured or inferred data type before performing comparisons. Normalization is intended to reduce false-positive changes caused by differences in representation, such as insignificant whitespace or compatible formatting.

Raw values from both the approved and incoming datasets are preserved alongside their normalized representations so that reviewers can inspect the exact source values that were received.

Normalization rules are type-aware and must not alter the semantic meaning of a value.



## 9. Field-Level Change Analysis

For every modified record, DataParity identifies the individual fields whose values differ between the approved and incoming versions.

Each detected field change records the previous value, incoming value, normalized values used for comparison, change type, and associated record identity.

Where meaningful for the field type, DataParity also calculates derived change information such as absolute difference, percentage difference, directional change, or date interval.

Field-level analysis describes the observed change without independently determining whether the change should be accepted or rejected. Risk and severity assessment is performed by a separate analysis layer using these change facts together with configured validation and business rules.

The raw source values are retained so that reviewers can inspect the exact values received.

## 10. Data Quality Validation

DataParity validates incoming dataset versions against the dataset's configured validation rules.

When a dataset is initially established, DataParity may infer candidate validation rules from the approved baseline, including data types, required fields, nullability, key uniqueness, and observed value characteristics.

Inferred rules are presented to the user for review and can be modified, accepted, or removed before they become active validation rules.

Validation rules are configuration associated with the logical dataset rather than hardcoded to specific fields or datasets in the application.

The validation engine applies active rules to incoming versions and produces structured validation findings when a rule is violated.

Validation failures are reported to the reviewer and do not automatically determine whether the dataset version is accepted or rejected.
Validation failures do not automatically reject a dataset version. When the dataset can still be reliably processed and compared, validation violations are recorded as findings and presented to the reviewer.

DataParity stops processing only when a condition prevents reliable analysis, comparison, or interpretation of the dataset. Examples include an unavailable configured record-identity key, an unrecoverable file structure, or other conditions where continuing could produce misleading analysis.

## 11. Risk & Severity Assessment

DataParity evaluates detected changes and validation findings using deterministic, explainable analysis rules.

Each finding is assigned one of four severity levels:

- `INFO`
- `LOW`
- `HIGH`
- `CRITICAL`

Severity is determined using relevant analysis signals such as field importance, magnitude of change, change direction, affected-record frequency, schema impact, record-identity impact, and validation violations.

Severity rules provide sensible defaults and may be customized as part of dataset configuration.

Every severity assignment includes an explanation identifying the relevant signals or rules that contributed to the classification.

For identical input data and identical configuration, severity assessment must be deterministic and produce consistent results.

Severity does not automatically determine whether a dataset version is approved or rejected. The reviewer remains responsible for the final decision.

## 12. Review & Approval

DataParity treats the dataset version as the primary unit of review and approval.

After processing and analysis, the reviewer can inspect the detected schema changes, record changes, field-level changes, validation findings, severity classifications, and explanations before making a decision.

The reviewer can either approve or reject the entire dataset version.

An approved version becomes the new active baseline for subsequent comparisons.

A rejected version does not replace the active baseline and remains available for historical inspection.

Approval may include an optional reviewer comment.

Rejection requires a reviewer-provided reason explaining why the dataset version was not accepted.

Every approval or rejection records the reviewer identity, decision, timestamp, and any associated comment or rejection reason.

## 13. Audit Trail

DataParity maintains an audit history for each dataset version to provide traceability and accountability for processing and review decisions.

The audit history records source-file metadata, processing status, comparison results, validation findings, severity assessments, reviewer decisions, reviewer identity, timestamps, and approval or rejection reasons.

Audit records reference the associated dataset version and source artifact rather than unnecessarily duplicating the complete dataset.

The audit trail must allow a user to understand what version was processed, what DataParity identified, and why the reviewer ultimately approved or rejected the version.

MVP retains audit history locally without imposing an application-level retention limit.

## 14. Export

DataParity allows users to export approved dataset versions separately from their associated analysis results.

Approved datasets can be exported in CSV or XLSX format without DataParity-specific annotations or analysis metadata being added to the business data.

Analysis results can be exported as machine-readable reports, including CSV and JSON formats, containing comparison summaries, field-level changes, validation findings, severity classifications, and review decisions.

Exports are generated from the approved or reviewed dataset version and its associated analysis results without modifying the stored source data or audit history.

## 15. Storage & Retention

DataParity is designed as a local-first application. Dataset files, normalized data, comparison results, validation findings, audit history, and review decisions are stored locally on the user's machine by default.

DataParity does not require customer datasets to be uploaded to or processed by DataParity-operated servers for core functionality.

The application maintains references between source files, dataset versions, analysis results, and audit records so that historical versions and review decisions can be inspected locally.

MVP does not impose an application-level retention limit on locally stored dataset history. Users remain responsible for managing local storage and retaining or deleting data according to their organizational requirements.

Future hosted or collaborative deployments may introduce configurable storage and retention policies without changing the core dataset and analysis model.

## 16. Error Handling

DataParity distinguishes between data findings, processing blockers, and unexpected application errors.

### 16.1 Data Findings

Data findings represent conditions discovered within an otherwise processable dataset, such as validation violations, unexpected values, duplicate records, or significant changes.

Data findings do not prevent analysis from continuing and are presented as structured findings for reviewer investigation.

### 16.2 Processing Blockers

Processing blockers are conditions that prevent DataParity from producing reliable analysis, such as unrecoverable file corruption, an unavailable configured record-identity column, or an unsupported structural condition.

When a processing blocker is encountered, DataParity stops the affected processing operation and provides an actionable explanation. The active approved baseline remains unchanged.

### 16.3 Application Errors

Unexpected application or infrastructure errors are treated separately from dataset findings and processing blockers.

DataParity must provide a clear technical error without misrepresenting an application failure as a problem with the customer's data.

Unexpected failures must not modify the active approved baseline or produce a misleading approval state.

## 17. Security & Privacy

DataParity follows a local-first security model in which customer datasets are processed and stored on the user's machine by default.

Core dataset processing does not require customer data to be transmitted to DataParity-operated servers. This minimizes exposure of potentially sensitive supplier, operational, financial, or business data.

DataParity must avoid transmitting dataset contents, comparison results, validation findings, or audit information unless the user explicitly enables a future feature that requires such transmission.

Local application storage must use appropriate filesystem permissions and database access controls to prevent unintended access by other users or processes.

Sensitive application data, including licensing credentials or other secrets, must not be stored in plaintext where a platform-provided secure credential mechanism is available.

Application logs must not unnecessarily contain raw dataset values, credentials, or other sensitive customer information.

The security model does not assume that local execution alone guarantees security. DataParity is responsible for minimizing unnecessary data exposure, protecting application-managed secrets, validating input files, and preventing unintended transmission of customer data.

Future hosted or collaborative deployments must introduce explicit authentication, authorization, encryption, and tenant-isolation controls appropriate to the deployment model.

## 18. Local-First Architecture

DataParity MVP is designed as a self-contained local application intended to run entirely on the user's machine.

The application consists of a React and TypeScript user interface, a Python and FastAPI application layer, a dedicated data-processing engine, local database storage, and local file storage.

The user interacts with DataParity through the application interface without requiring knowledge of Python, databases, command-line tools, or server administration.

The application is responsible for starting and managing its local runtime components as part of the normal application lifecycle.

The processing engine remains independent from the user interface so that ingestion, normalization, validation, record matching, comparison, change analysis, and risk assessment can be tested and evolved independently.

The persistence layer is abstracted from the processing engine so that the MVP can use local storage while future hosted deployments can introduce alternative persistence implementations without changing the core analysis model.

The local application must operate without a dependency on DataParity-operated cloud infrastructure for core dataset ingestion, comparison, validation, review, or export functionality.

The distributed application must provide a self-contained runtime so that end users are not required to install Python, Node.js, database servers, package managers, or other development dependencies.

Installation and first launch must provide a usable DataParity environment without requiring command-line configuration or developer tooling.

## 19. Licensing

DataParity uses a license-based entitlement model for commercial distribution.

A purchased license grants the customer access to the corresponding DataParity product or plan. License credentials are treated as sensitive application data and must not be stored in plaintext where a platform-provided secure credential mechanism is available.

License activation may require an internet connection, but core dataset processing and application functionality do not depend on continuous connectivity after successful activation.

The licensing system is independent of the payment provider. DataParity must not couple its core application logic to a specific payment processor.

The licensing architecture must support future product plans, license expiration, activation limits, and revocation without requiring changes to the core dataset processing model.

## 20. Non-Goals

The following capabilities are outside the scope of the DataParity MVP:

- Real-time or continuously streaming data ingestion.
- Direct integrations with supplier, ERP, CRM, marketplace, or other external data systems.
- Automatic business decisions or automatic approval/rejection of dataset versions.
- Full ETL, data warehouse, or general-purpose data transformation functionality.
- Arbitrary or unsupported file formats beyond the defined MVP ingestion formats.
- Multi-user collaborative review and cloud-based synchronization.
- Hosted centralized processing of customer datasets.
- Complex workflow automation beyond the dataset review and approval lifecycle.
- Opaque or non-deterministic AI-based decisions as the primary mechanism for validation, comparison, or severity assessment.
- Advanced statistical anomaly detection beyond the deterministic analysis required by the MVP.

## 21. MVP Acceptance Criteria

The DataParity MVP is considered functionally complete when a non-technical user can:

1. Install and launch the application without manually installing Python, Node.js, a database server, package managers, or other development dependencies.
2. Create a logical dataset and import a supported CSV or XLSX file.
3. Select a worksheet when an XLSX file contains multiple worksheets.
4. Configure or confirm the dataset's record identity, including composite keys.
5. Review and configure validation rules inferred from the initial approved dataset.
6. Approve an initial dataset version as the active baseline.
7. Import a subsequent dataset version for analysis.
8. Detect and review schema changes and data-type changes.
9. Classify records as added, removed, unchanged, or modified.
10. Inspect field-level changes including previous and incoming values.
11. Identify data-quality and validation findings.
12. Assign deterministic and explainable `INFO`, `LOW`, `HIGH`, or `CRITICAL` severity levels to findings.
13. Review the complete analysis and approve or reject the dataset version.
14. Provide a reason when rejecting a dataset version.
15. Inspect historical dataset versions, analysis results, and review decisions.
16. Export an approved dataset in CSV or XLSX format.
17. Export associated analysis results in CSV or JSON format.
18. Operate core functionality locally without transmitting customer dataset contents to DataParity-operated infrastructure.