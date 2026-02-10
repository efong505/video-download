# DynamoDB Query Guide - Election System

Complete guide for querying and managing election data in DynamoDB using AWS Console and CLI.

## Table of Contents
- [AWS Console Methods](#aws-console-methods)
- [AWS CLI Commands](#aws-cli-commands)
- [Common Query Patterns](#common-query-patterns)
- [Update Operations](#update-operations)

---

## AWS Console Methods

### Viewing All Items in a Table

1. Go to **DynamoDB** in AWS Console
2. Click **Tables** → Select your table (e.g., `candidates`, `races`, `contributors`, `election-events`)
3. Click **Explore table items**
4. All items will be displayed

### Filtering Items

1. In the **Explore table items** view
2. Click **Scan/Query items**
3. Click **Scan** tab
4. Add filters:
   - Click **Add filter**
   - Select attribute (e.g., `state`)
   - Choose operator (e.g., `=`, `contains`)
   - Enter value
5. Click **Run**

### Editing an Item

1. Find the item in **Explore table items**
2. Click on the item's primary key (e.g., `candidate_id`)
3. Click **Edit** button
4. Modify field values
5. Click **Save changes**

### Example: Find Nebraska City Council Races

1. Go to **races** table
2. Click **Explore table items** → **Scan/Query items**
3. Add filter: `state = Nebraska`
4. Add filter: `office contains Council`
5. Click **Run**

---

## AWS CLI Commands

### List All Items in a Table

```bash
# Scan entire table
aws dynamodb scan --table-name candidates

# Scan with specific attributes only
aws dynamodb scan \
  --table-name candidates \
  --projection-expression "candidate_id, #n, #st, office" \
  --expression-attribute-names '{"#n": "name", "#st": "state"}'
```

### Filter by State

```bash
# Get all candidates from Nebraska
aws dynamodb scan \
  --table-name candidates \
  --filter-expression "#st = :state" \
  --expression-attribute-names '{"#st": "state"}' \
  --expression-attribute-values '{":state": {"S": "Nebraska"}}'
```

### Filter by Multiple Conditions

```bash
# Get Nebraska City Council races
aws dynamodb scan \
  --table-name races \
  --filter-expression "#st = :state AND contains(office, :office)" \
  --expression-attribute-names '{"#st": "state"}' \
  --expression-attribute-values '{":state": {"S": "Nebraska"}, ":office": {"S": "Council"}}'
```

### Get Specific Item by ID

```bash
# Get candidate by candidate_id
aws dynamodb get-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID_HERE"}}'

# Get race by race_id
aws dynamodb get-item \
  --table-name races \
  --key '{"race_id": {"S": "YOUR_RACE_ID_HERE"}}'
```

---

## Common Query Patterns

### Find All Races for a Specific State

**Console:**
- Table: `races`
- Filter: `state = Nebraska`

**CLI:**
```bash
aws dynamodb scan \
  --table-name races \
  --filter-expression "#st = :state" \
  --expression-attribute-names '{"#st": "state"}' \
  --expression-attribute-values '{":state": {"S": "Nebraska"}}'
```

### Find Candidates by Office

**Console:**
- Table: `candidates`
- Filter: `office contains Mayor`

**CLI:**
```bash
aws dynamodb scan \
  --table-name candidates \
  --filter-expression "contains(office, :office)" \
  --expression-attribute-values '{":office": {"S": "Mayor"}}'
```

### Find Candidates Without a Race Assignment

**Console:**
- Table: `candidates`
- Filter: `race_id = null` OR `attribute_not_exists(race_id)`

**CLI:**
```bash
aws dynamodb scan \
  --table-name candidates \
  --filter-expression "attribute_not_exists(race_id) OR race_id = :null" \
  --expression-attribute-values '{":null": {"NULL": true}}'
```

### Find Verified Contributors

**Console:**
- Table: `contributors`
- Filter: `verified = true`

**CLI:**
```bash
aws dynamodb scan \
  --table-name contributors \
  --filter-expression "verified = :verified" \
  --expression-attribute-values '{":verified": {"BOOL": true}}'
```

---

## Update Operations

### Update a Single Field

```bash
# Update candidate's race_id
aws dynamodb update-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID"}}' \
  --update-expression "SET race_id = :race_id" \
  --expression-attribute-values '{":race_id": {"S": "YOUR_RACE_ID"}}'
```

### Update Multiple Fields

```bash
# Update candidate name and office
aws dynamodb update-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID"}}' \
  --update-expression "SET #n = :name, office = :office" \
  --expression-attribute-names '{"#n": "name"}' \
  --expression-attribute-values '{":name": {"S": "John Smith"}, ":office": {"S": "Governor"}}'
```

### Update with Reserved Keywords

DynamoDB reserved keywords (like `name`, `state`, `status`) require ExpressionAttributeNames:

```bash
aws dynamodb update-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID"}}' \
  --update-expression "SET #n = :name, #st = :state, #s = :status" \
  --expression-attribute-names '{"#n": "name", "#st": "state", "#s": "status"}' \
  --expression-attribute-values '{":name": {"S": "Jane Doe"}, ":state": {"S": "Texas"}, ":status": {"S": "active"}}'
```

### Set Field to Null (Unassign Race)

```bash
# Remove race assignment from candidate
aws dynamodb update-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID"}}' \
  --update-expression "SET race_id = :null" \
  --expression-attribute-values '{":null": {"NULL": true}}'
```

### Delete an Item

```bash
# Delete a candidate
aws dynamodb delete-item \
  --table-name candidates \
  --key '{"candidate_id": {"S": "YOUR_CANDIDATE_ID"}}'

# Delete a race
aws dynamodb delete-item \
  --table-name races \
  --key '{"race_id": {"S": "YOUR_RACE_ID"}}'
```

---

## Tips and Best Practices

### Reserved Keywords
Always use ExpressionAttributeNames for these common reserved words:
- `name`, `state`, `status`, `data`, `date`, `time`, `year`, `month`, `day`

### Data Types in CLI
- String: `{"S": "value"}`
- Number: `{"N": "123"}`
- Boolean: `{"BOOL": true}`
- Null: `{"NULL": true}`
- List: `{"L": [{"S": "item1"}, {"S": "item2"}]}`
- Map: `{"M": {"key1": {"S": "value1"}}}`

### Scan vs Query
- **Scan**: Examines every item (slower, more expensive)
- **Query**: Uses primary key or index (faster, cheaper)
- Use Query when possible, Scan for filtering by non-key attributes

### Admin Panel (Easiest Method)
For most operations, use the admin panel at `admin-contributors.html`:
- Built-in filters for state and office
- Edit buttons for all items
- Visual interface for managing data
- No need to remember CLI syntax

---

## Quick Reference

| Task | Console | CLI |
|------|---------|-----|
| View all items | Explore table items | `aws dynamodb scan --table-name TABLE` |
| Filter by state | Add filter: state = VALUE | `--filter-expression "#st = :state"` |
| Get by ID | Click on item | `aws dynamodb get-item --key {...}` |
| Update field | Edit → Save | `aws dynamodb update-item --update-expression "SET..."` |
| Delete item | Actions → Delete | `aws dynamodb delete-item --key {...}` |

---

## Example Workflows

### Workflow 1: Link Candidate to Race

1. **Find the race_id:**
   ```bash
   aws dynamodb scan --table-name races \
     --filter-expression "#st = :state AND office = :office" \
     --expression-attribute-names '{"#st": "state"}' \
     --expression-attribute-values '{":state": {"S": "Nebraska"}, ":office": {"S": "Mayor (Omaha)"}}'
   ```

2. **Update candidate with race_id:**
   ```bash
   aws dynamodb update-item --table-name candidates \
     --key '{"candidate_id": {"S": "CANDIDATE_ID"}}' \
     --update-expression "SET race_id = :race_id" \
     --expression-attribute-values '{":race_id": {"S": "RACE_ID_FROM_STEP_1"}}'
   ```

### Workflow 2: Find Unassigned Candidates

1. **Scan for null race_id:**
   ```bash
   aws dynamodb scan --table-name candidates \
     --filter-expression "attribute_not_exists(race_id)"
   ```

2. **Fix in admin panel:**
   - Go to admin-contributors.html
   - Click Candidates tab
   - Click Edit on unassigned candidate
   - Select race from dropdown
   - Save

---

## Troubleshooting

### Error: ValidationException - Reserved keyword
**Solution:** Use ExpressionAttributeNames
```bash
--expression-attribute-names '{"#n": "name", "#st": "state"}'
```

### Error: Item not found
**Solution:** Verify the primary key value is correct
```bash
# Check if item exists
aws dynamodb get-item --table-name TABLE --key '{"id": {"S": "VALUE"}}'
```

### Scan returns no results
**Solution:** Check filter syntax and data types
```bash
# Verify attribute names and values match exactly
aws dynamodb scan --table-name TABLE --filter-expression "attribute = :val"
```
