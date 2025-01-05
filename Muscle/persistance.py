
from datetime import datetime
import json
from typing import Tuple


class Data:
    def __init__(self):
        self.schedule_file = r'assets/data/schedule.json'
        self.current_place_file = r'assets/data/current_place_in_schedule.json'

        with open(self.schedule_file, 'r') as f:
            self.schedule = json.load(f)

        with open(self.current_place_file, 'r') as f:
            self.current_place_in_schedule = json.load(f)

    def save_schedule_reps_and_kilos(self):
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, fp=f, indent=4)
        try:
            with open(r'/storage/sdcard0/Documents/muscle_app_current_schedule.json', 'x') as g:
                json.dump(self.schedule, fp=g, indent=4)
        except:
            pass

    def save_current_place_in_schedule(self):
        with open(self.current_place_file, 'w') as f:
            json.dump(self.current_place_in_schedule, fp=f, indent=4)


class ExerciseData:
    def __init__(self):
        data = Data()
        self.data = data
        self.schedule = data.schedule
        self.current_place_in_schedule = data.current_place_in_schedule
        '''
        self.program = program
        self.stage = self.get_stage_str(stage)
        self.week = self.get_week_str(self.stage, week)
        self.workout = self.get_workout_str(workout)
        self.circuit, self.exercise_index = self.get_circuit_and_exercise_index(exercise_index)
        '''
        self.program = self.current_place_in_schedule['program']
        self.stage = self.get_stage_str(self.current_place_in_schedule['stage'])
        self.week = self.get_week_str(self.stage, self.current_place_in_schedule['week'])
        self.workout = self.get_workout_str(self.current_place_in_schedule['workout'])
        self.circuit = self.get_circuit_str(self.current_place_in_schedule['circuit'])
        self.exercise_index = self.current_place_in_schedule['exercise']

    def save(self):
        self.data.save_schedule_reps_and_kilos()
        self.data.current_place_in_schedule['program'] = self.program
        self.data.current_place_in_schedule['stage'] = self.get_stage_int()
        self.data.current_place_in_schedule['week'] = self.get_week_int()
        self.data.current_place_in_schedule['workout'] = self.get_workout_int()
        self.data.current_place_in_schedule['circuit'] = self.get_circuit_int()
        self.data.current_place_in_schedule['exercise'] = self.exercise_index
        self.data.save_current_place_in_schedule()

    @staticmethod
    def get_workout_str(workout: int) -> str:
        return f'workout {workout}'

    def get_workout_int(self) -> int:
        return int(self.workout.split(' ')[1])

    @staticmethod
    def get_stage_str(stage: int) -> str:
        return f'stage {stage}'

    def get_stage_int(self) -> int:
        return int(self.stage.split(' ')[1])

    @staticmethod
    def get_week_str(stage: str, week: int) -> str:
        if stage == 'stage 1':
            return f'week {week}'
        elif stage == 'stage 2':
            return f'week {week + 7}'
        elif stage == 'stage 3':
            return f'week {week + 14}'
        elif stage == 'stage 4':
            return f'week {week + 21}'

    def get_week_int(self) -> int:
        if self.stage == 'stage 1':
            return int(self.week.split(' ')[1])
        elif self.stage == 'stage 2':
            return int(self.week.split(' ')[1]) - 7
        elif self.stage == 'stage 3':
            return int(self.week.split(' ')[1]) - 14
        elif self.stage == 'stage 4':
            return int(self.week.split(' ')[1]) - 21

    @staticmethod
    def get_circuit_str(circuit: int) -> str:
        return f'circuit {circuit}'

    def get_circuit_int(self) -> int:
        return int(self.circuit.split(' ')[1])

    def get_circuit_and_exercise_index(self, exercise_index) -> \
            Tuple[str, int]:
        circuits = self.schedule[self.program][self.stage][self.week][self.workout]
        if len(circuits) > 1:
            i = 0
            for mc in range(1, len(circuits) + 1):
                num_of_exercises = len(circuits[f'circuit {mc}']['name'])
                for ex_index in range(0, num_of_exercises):
                    i += 1
                    if i == exercise_index:
                        return f'circuit {mc}', ex_index

        return 'circuit 1', exercise_index

    def to_next_ex(self):
        exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

        if self.exercise_index < len(exercises['name']) - 1:
            self.exercise_index += 1
        elif self.exercise_index == len(exercises['name']) - 1:
            self.exercise_index = 0

    def to_previous_ex(self):
        exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

        if self.exercise_index > 0:
            self.exercise_index -= 1
        elif self.exercise_index == 0:
            self.exercise_index = len(exercises['name']) - 1

    def to_next_circ(self):
        self.exercise_index = 0
        circ_int = int(self.circuit.split(' ')[1])
        circuits = self.schedule[self.program][self.stage][self.week][self.workout]

        if circ_int < len(circuits):
            circ_int += 1
        elif circ_int == len(circuits):
            circ_int = 1

        self.circuit = f'circuit {circ_int}'

    def to_previous_circ(self):
        self.exercise_index = 0
        circ_int = int(self.circuit.split(' ')[1])
        circuits = self.schedule[self.program][self.stage][self.week][self.workout]

        if circ_int > 1:
            circ_int -= 1
        elif circ_int == 1:
            circ_int = len(circuits)

        self.circuit = f'circuit {circ_int}'

    def update_program(self, new_program: str):
        self.program = new_program
        self.stage = self.get_stage_str(1)
        self.week = self.get_week_str(self.stage, 1)
        self.workout = self.get_workout_str(1)
        self.circuit, self.exercise_index = self.get_circuit_and_exercise_index(0)

    def update_stage(self, new_stage: int):
        self.stage = self.get_stage_str(new_stage)
        self.week = self.get_week_str(self.stage, 1)
        self.workout = self.get_workout_str(1)
        self.circuit, self.exercise_index = self.get_circuit_and_exercise_index(0)

    def update_week(self, new_week: int):
        self.week = self.get_week_str(self.stage, new_week)
        self.workout = self.get_workout_str(1)
        self.circuit, self.exercise_index = self.get_circuit_and_exercise_index(0)

    def update_workout(self, new_workout: int):
        self.workout = self.get_workout_str(new_workout)
        self.circuit, self.exercise_index = self.get_circuit_and_exercise_index(1)

    def save_exercise_time_and_day(self):
        now = str(datetime.now())
        exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]
        exercises['work sets done'][self.exercise_index] = now
