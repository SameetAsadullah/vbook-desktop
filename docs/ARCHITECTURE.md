# Architecture

VBook separates the user interface, business objects, and persistence concerns into three packages. This document describes the existing design without changing the original implementation.

## Presentation layer

`presentationLayer` contains the JavaFX entry point, controllers, FXML views, CSS, and image assets. Screens are grouped by user role:

- `Admin` manages customer, vendor, receptionist, and hotel records.
- `Receptionist` handles hotel registration and front-desk workflows.
- `User` covers customer registration, hotel selection, and reservations.
- `Vendor` covers vendor registration and hotel advertising.

`presentationLayer.Main` starts the application and loads `HomePage.fxml`.

## Logic layer

`logicLayer` contains the domain model:

- `HRS` coordinates application data.
- `Admin`, `Customer`, `Receptionist`, and `Vendor` represent system users.
- `Hotel`, `Room`, and `Reservation` represent the booking domain.

The JavaFX controllers call these classes to perform role-specific operations.

## Data layer

`dataLayer.writerAndReader` serializes records to CSV files and reads them back into the domain model. The files are created beneath `src/dataLayer` at runtime and are excluded from version control to avoid publishing local account or reservation data.

## Runtime flow

```text
JavaFX view → controller → logic-layer model → CSV reader/writer
```

This compact architecture implements object-oriented domain modeling and multi-role desktop workflows. It also leaves clear extension points for database-backed persistence and a dedicated service layer.
