# Database ER Diagram

## MongoDB Collections Schema

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Users       │       │    Projects     │       │     Tasks       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ _id (ObjectId)  │◄──────┼ created_by      │       │ _id (ObjectId)  │
│ name (String)   │       │ _id (ObjectId)  │       │ title (String)  │
│ email (String)  │       │ name (String)   │       │ description     │
│ password_hash   │       │ description     │       │ (String)        │
│ role (String)   │       │ status (String) │       │ status (String) │
│ created_at      │       │ deadline (Date) │       │ priority        │
│                 │       │ team [ObjectId] │◄──────┼ (String)        │
│                 │       │ created_at      │       │ assigned_to     │
│                 │       │ updated_at      │       │ (ObjectId)      │
└─────────────────┘       └─────────────────┘       │ project_id      │
                                                    │ (ObjectId)      │
                                                    │ deadline (Date) │
                                                    │ comments [String│
                                                    │ created_at      │
                                                    │ updated_at      │
                                                    └─────────────────┘
```

## Relationships

### One-to-Many Relationships:
- **Users → Projects**: One user can create many projects (`created_by`)
- **Users → Tasks**: One user can be assigned to many tasks (`assigned_to`)
- **Projects → Tasks**: One project can have many tasks (`project_id`)
- **Projects → User Stories**: One project can have multiple AI-generated user story sets (`project_id`)

### Many-to-Many Relationships:
- **Users ↔ Projects**: Users can be part of multiple project teams (`team` array in Projects)

## Key Relationships:

1. **User creates Project**: `Projects.created_by` → `Users._id`
2. **User assigned to Task**: `Tasks.assigned_to` → `Users._id`
3. **Task belongs to Project**: `Tasks.project_id` → `Projects._id`
4. **Users in Project Team**: `Projects.team` → `Users._id` (array)

## Indexes Recommended:

```javascript
// Users collection
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "role": 1 })

// Projects collection
db.projects.createIndex({ "created_by": 1 })
db.projects.createIndex({ "status": 1 })
db.projects.createIndex({ "deadline": 1 })

// Tasks collection
db.tasks.createIndex({ "assigned_to": 1 })
db.tasks.createIndex({ "project_id": 1 })
db.tasks.createIndex({ "status": 1 })
db.tasks.createIndex({ "deadline": 1 })

// User Stories collection
db.user_stories.createIndex({ "project_id": 1 })
db.user_stories.createIndex({ "generated_at": 1 })
```

## Data Flow:

1. **Authentication**: User logs in → JWT token generated
2. **Project Creation**: User creates project → Project linked to creator
3. **Task Assignment**: Tasks created under projects → Assigned to team members
4. **Team Management**: Users added to project teams → Can be assigned tasks
5. **Reporting**: Aggregate data from all collections for dashboard analytics</content>
<parameter name="filePath">c:\Users\manimaddy\curus_Health\curus_Health\project-management-tool\ER_DIAGRAM.md
