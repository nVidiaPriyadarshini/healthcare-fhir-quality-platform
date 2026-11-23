# Architecture
Three tiers: React + TypeScript + Vite dashboard; FastAPI REST API; PostgreSQL 16 persistence through SQLAlchemy.
Incoming JSON is checked for supported type (Patient, Observation, Encounter), required/recommended fields, selected R4 code values, and reference shape. Weighted score: completeness 30%, validity 50%, consistency 20%; uniqueness is reported separately and duplicate persisted IDs are rejected.
These starter checks are not a complete HL7 FHIR conformance validator. Production needs official R4 StructureDefinition/profile validation, terminology service, reference resolution, audit controls, authentication/authorization, encryption, retention policies, and migrations.
Only fictional synthetic records are included. Never load identifiable patient data into this demo.
