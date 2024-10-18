from marshmallow import Schema, fields

class TaskSchema(Schema):
    """작업 스키마"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    done = fields.Boolean()

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)