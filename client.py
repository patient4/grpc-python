import grpc
import todo_pb2
import todo_pb2_grpc

channel = grpc.insecure_channel('localhost:5001')
stub = todo_pb2_grpc.TodoServiceStub(channel)

response = stub.CreateTodo(todo_pb2.CreateTodoRequest(title="Buy Milk", description="Buy 2 liters of milk"))
response2 = stub.CreateTodo(todo_pb2.CreateTodoRequest(title="sell Milk", description="sell 2 liters of milk"))
print("response: ", response," \nresponse2: ", response2)
response3 = stub.GetTodos(todo_pb2.Empty())
print("\n Response3: ",response3)

responsedelete = stub.DeleteAllTodos(todo_pb2.Empty())
print("\n Response3: ",responsedelete)

response3 = stub.GetTodos(todo_pb2.Empty())
print("\n Response3: ",response3)