import grpc
from concurrent import futures
import time
import todo_pb2
import todo_pb2_grpc

# In-memory storage for Todos (for simplicity)
todos = []

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    def CreateTodo(self, request, context):
        print(request, "request", " \ncontext", context)
        todo_id = len(todos) + 1
        todo = todo_pb2.Todo(
            id=todo_id,
            title=request.title,
            description=request.description,
            completed=False
        )
        todos.append(todo)
        return todo_pb2.TodoResponse(success=True, message="Todo created", todo=todo)

    def GetTodos(self, request, context):
        return todo_pb2.GetTodosResponse(todos=todos)

    def MarkTodoCompleted(self, request, context):
        todo = next((t for t in todos if t.id == request.id), None)
        if todo:
            todo.completed = True
            return todo_pb2.TodoResponse(success=True, message="Todo marked as completed", todo=todo)
        return todo_pb2.TodoResponse(success=False, message="Todo not found")

    def DeleteTodo(self, request, context):
        global todos
        todo = next((t for t in todos if t.id == request.id), None)
        if todo:
            todos = [t for t in todos if t.id != request.id]
            return todo_pb2.TodoResponse(success=True, message="Todo deleted", todo=todo)
        return todo_pb2.TodoResponse(success=False, message="Todo not found")

    def DeleteAllTodos(self, request, context):
        global todos
        todos.clear()
        return todo_pb2.DeleteAllTodosResponse(success=True, message="Deleted all Todos.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:5001')
    print("Starting gRPC server on port 5001...")
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
