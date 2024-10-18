from flask_restx import Namespace, Resource, fields
from app.controllers.task_controller import TaskController
from flask import current_app as app

api = Namespace('tasks', description='Task operations')

# API 모델 정의
task_model = api.model('Task', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task title'),
    'description': fields.String(description='The task description'),
    'done': fields.Boolean(description='The task status')
})

@api.route('/')
class TaskList(Resource):
    @api.doc('list_tasks')
    @api.marshal_list_with(task_model)
    def get(self):
        """모든 작업을 조회"""
        app.logger.info('Fetching all tasks')
        return TaskController.get_all_tasks()

    @api.doc('create_task')
    @api.expect(task_model)
    @api.marshal_with(task_model, code=201)
    def post(self):
        """새 작업을 생성"""
        app.logger.info('Creating a new task')
        return TaskController.create_task(api.payload), 201

@api.route('/<int:id>')
@api.param('id', 'The task identifier')
@api.response(404, 'Task not found')
class Task(Resource):
    @api.doc('get_task')
    @api.marshal_with(task_model)
    def get(self, id):
        """특정 작업을 조회"""
        app.logger.info(f'Fetching task with id: {id}')
        task = TaskController.get_task(id)
        return task if task else api.abort(404, f"Task {id} doesn't exist")

    @api.doc('update_task')
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self, id):
        """작업을 수정"""
        app.logger.info(f'Updating task with id: {id}')
        task = TaskController.update_task(id, api.payload)
        return task if task else api.abort(404, f"Task {id} doesn't exist")

    @api.doc('delete_task')
    @api.response(204, 'Task deleted')
    def delete(self, id):
        """작업을 삭제"""
        app.logger.info(f'Deleting task with id: {id}')
        if TaskController.delete_task(id):
            return '', 204
        api.abort(404, f"Task {id} doesn't exist")