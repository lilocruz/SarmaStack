import os
import yaml

class StateTracker:
    DEFAULT_STATE_FILE = 'state.srstate'

    def __init__(self, state_file=None):
        self.state_file = state_file or self.DEFAULT_STATE_FILE
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = yaml.safe_load(f)
                    return state if state is not None else {}
            except FileNotFoundError:
                pass
        return {}

    def save_state(self):
        with open(self.state_file, 'w') as f:
            yaml.safe_dump(self.state, f)

    def get_resource_state(self, resource_type, resource_name):
        if resource_type in self.state:
            resource_state = self.state[resource_type]
            return resource_state.get(resource_name)
        return None

    def update_resource_state(self, resource_type, resource_name, resource_state):
        if resource_type not in self.state:
            self.state[resource_type] = {}
        self.state[resource_type][resource_name] = resource_state
        self.save_state()

    def resource_exists(self, resource_type, resource_name):
        return resource_name in self.state.get(resource_type, {})

    def create_state_file(self):
        with open(self.state_file, 'w') as f:
            f.write('')

    def delete_state_file(self):
        os.remove(self.state_file)
