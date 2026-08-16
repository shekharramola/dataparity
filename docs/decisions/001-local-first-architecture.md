# ADR-001: Local-First Architecture

## Status

Accepted

## Context

DataParity processes potentially sensitive recurring datasets received from
suppliers, partners, or internal data sources.

The MVP is intended to be a plug-and-play application for non-technical users.
Users should not be required to install or manage Python, Node.js, database
servers, or other development infrastructure.

Customer dataset contents should also remain on the user's machine by default.
Core ingestion, validation, comparison, analysis, review, and export should not
depend on DataParity-operated cloud infrastructure.

## Decision

DataParity MVP will use a local-first architecture.

The distributed application will contain the required runtime components and
will execute core dataset processing locally on the user's machine.

The primary application architecture consists of:

- React and TypeScript for the user interface.
- FastAPI for the local application/API layer.
- A dedicated processing engine for ingestion, normalization, validation,
  record matching, comparison, change analysis, and severity assessment.
- Local persistence for application metadata, review state, and audit history.
- Local filesystem storage for source files and generated artifacts.

The processing engine will remain independent of the presentation layer and
will not depend directly on React or FastAPI.

Core dataset functionality must not require customer dataset contents to be
transmitted to DataParity-operated infrastructure.

Future hosted or enterprise deployments may introduce centralized services
without changing the core dataset comparison and analysis model.

## Rationale

A local-first architecture provides:

- Stronger data privacy by minimizing unnecessary data transmission.
- A simpler deployment model for non-technical users.
- No mandatory cloud infrastructure for the MVP.
- Lower operational cost during early development and distribution.
- A clear separation between the core analysis engine and deployment model.

The architecture also allows the same processing capabilities to be reused in
future hosted deployments.

## Consequences

### Positive

- Customer data remains local by default.
- The MVP can operate without a cloud account.
- The application can be packaged as a self-contained desktop application.
- Development and testing can be performed without production infrastructure.
- The core processing engine can later support alternative deployment models.

### Negative

- DataParity must provide reliable local storage and backup behavior.
- Desktop application packaging becomes an important engineering concern.
- Multi-user collaboration is not part of the MVP.
- Centralized synchronization is not available in the local-first MVP.

## Alternatives Considered

### Cloud-First Architecture

Rejected for the MVP because it would require customer datasets to be uploaded
for core processing and would introduce unnecessary infrastructure and
operational costs.

### Local Client With Mandatory Remote Processing

Rejected because it would conflict with the privacy and offline-first goals of
the MVP.
