from util import Stack, Queue

class Game:
    def find_path_to(self, starting_room_id, target_id, adj):
        queue = Queue()
        final_path = None
        visited = set()
        queue.enqueue([starting_room_id])
        while queue.len() > 0:
            path = queue.dequeue()
            vert = path[-1]
            if vert not in visited:
                if vert == target_id:
                   final_path = path
                   break
                visited.add(vert)
                for room in adj[vert].items():
                    new_path = list(path)
                    new_path.append(room)
                    queue.enqueue(new_path)
        if final_path is None:
            return
        new_path = []
        for idx, room in enumerate(final_path):
            if idx > 0:
                lastRoom = final_path[idx - 1]
                for direction in adj[lastRoom]:
                    if adj[lastRoom][direction] == room:
                        new_path.append({'dir': direction, 'next_room': room})
        return new_path
