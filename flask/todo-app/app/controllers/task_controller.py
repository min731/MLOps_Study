from app.models.task import Task
from app.schemas.task_schema import task_schema, tasks_schema
from app import db

class TaskController:
    """작업 컨트롤러"""

    @staticmethod
    def get_all_tasks():
        """모든 작업을 조회"""
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    @staticmethod
    def get_task(task_id):
        """특정 작업을 조회"""
        task = Task.query.get(task_id)
        return task_schema.dump(task) if task else None

    @staticmethod
    def create_task(data):
        """새 작업을 생성"""
        task = Task(**task_schema.load(data))
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task)

    @staticmethod
    def update_task(task_id, data):
        """작업을 수정"""
        task = Task.query.get(task_id)
        if task:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.done = data.get('done', task.done)
            db.session.commit()
            return task_schema.dump(task)
        return None

    @staticmethod
    def delete_task(task_id):
        """작업을 삭제"""
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False