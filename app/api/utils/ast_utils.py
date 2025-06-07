from celery import chain, chord
import ast
from app.shared.enums.operation_type import OperationType
from app.shared.enums.worker_queue import WorkerQueue
from app.worker.celery_consumer import add, subtract, multiply, divide, xsum
import operator

OP_MAP = {
    ast.Add: add,
    ast.Sub: subtract,
    ast.Mult: multiply,
    ast.Div: divide,
}

OP_QUEUE = {
    ast.Add: WorkerQueue.ADD_QUEUE,
    ast.Sub: WorkerQueue.SUBTRACT_QUEUE,
    ast.Mult: WorkerQueue.MULTIPLY_QUEUE,
    ast.Div: WorkerQueue.DIVIDE_QUEUE,
}

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}

def build_chain_mutable(node):
    if isinstance(node, ast.BinOp):
        left = build_chain_mutable(node.left)
        right = build_chain_mutable(node.right)

        op_type = type(node.op)
        op = OP_MAP[op_type]
        op_queue = OP_QUEUE[op_type]

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return op.s(left, right).set(queue=op_queue)

        return chain(
            left,
            op.s(right).set(queue=op_queue)
        )
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        raise ValueError(f"Unsupported node: {ast.dump(node)}")
    
def build_chain_immutable(node):
    if isinstance(node, ast.BinOp):
        left, prev1 = build_chain_immutable(node.left)
        right, _ = build_chain_immutable(node.right)

        op_type = type(node.op)
        if op_type not in ops:
            raise ValueError(f"Unsupported op")
        
        op = OP_MAP[op_type]
        op_queue = OP_QUEUE[op_type]

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            prev = ops[op_type](left, right)
            return op.si(left, right).set(queue=op_queue), prev

        return chain(
            left,
            op.si(prev1, right).set(queue=op_queue)
        ), ops[op_type](prev1, right)
    elif isinstance(node, ast.Constant):
        return node.value, 0
    else:
        raise ValueError(f"Unsupported node: {ast.dump(node)}")
    

def build_shorthand_chaining(node):
    if isinstance(node, ast.BinOp):
        left = build_shorthand_chaining(node.left)
        right = build_shorthand_chaining(node.right)

        op_type = type(node.op)
        op = OP_MAP[op_type]
        op_queue = OP_QUEUE[op_type]

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return op.s(left, right).set(queue=op_queue)

        return left | op.s(right).set(queue=op_queue)
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        raise ValueError(f"Unsupported node: {ast.dump(node)}")
   
def build_chord():
    return chord(
                header=[
                    add.s(1, 1).set(queue=WorkerQueue.ADD_QUEUE),
                    add.s(2, 2).set(queue=WorkerQueue.ADD_QUEUE),
                    add.s(9, 9).set(queue=WorkerQueue.ADD_QUEUE)
                ],
                body=xsum.s().set(queue=WorkerQueue.ADD_QUEUE)
            )

def build_chord_with_callback():
    callback = xsum.s().set(queue=WorkerQueue.ADD_QUEUE)
    return chord(
                header=[
                    add.s(1, 1).set(queue=WorkerQueue.ADD_QUEUE),
                    add.s(2, 2).set(queue=WorkerQueue.ADD_QUEUE),
                    add.s(9, 9).set(queue=WorkerQueue.ADD_QUEUE)
                ]
            )(callback)

def extract_expression(expression: str, operation_type: OperationType):
    tree = ast.parse(expression, mode='eval')
    match operation_type:
        case OperationType.MUTABLE:
            return build_chain_mutable(tree.body)
        case OperationType.IMMUTABLE:
            return build_chain_immutable(tree.body)[0]
        case OperationType.SHORTHAND_CHAINING:
            return build_shorthand_chaining(tree.body)
        case OperationType.CHORD:
            return build_chord()
        case OperationType.CHORD_WITH_CALLBACK:
            return build_chord_with_callback()
    return None
