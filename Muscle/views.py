import os
from typing import Callable

import flet as ft
from persistance import ExerciseData


class InfoView:
    def __init__(self, ex_data: ExerciseData, update_program: Callable, update_stage: Callable,
                 update_week: Callable, update_workout: Callable):
        self.ex_data = ex_data
        self.schedule = ex_data.schedule
        self.program = ex_data.program
        self.stage = ex_data.stage
        self.week = ex_data.week
        self.workout = ex_data.workout
        self.circuit = ex_data.circuit
        self.exercise_index = ex_data.exercise_index

        self.exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

        self.update_stage = update_stage
        self.update_week = update_week
        self.update_workout = update_workout
        self.update_program = update_program

    def generate_view(self, page):
        page.add(

            ft.Row(controls=[ft.Text('PROGRAM  ', size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('beginner'), ft.dropdown.Option('intermediate'),
                                                  ft.dropdown.Option('advanced')],
                                         value=str(self.ex_data.program), dense=True, select_icon_size=1,
                                         width=100, height=50, on_change=self.update_program),
                             ft.Text('STAGE         ', size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('1'), ft.dropdown.Option('2'),
                                                  ft.dropdown.Option('3'), ft.dropdown.Option('4')],
                                         value=str(self.ex_data.get_stage_int()),
                                         width=60, height=50, on_change=self.update_stage)
                             ]),
            ft.Row(controls=[ft.Text('WEEK          ', size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('1'), ft.dropdown.Option('2'),
                                                  ft.dropdown.Option('3'), ft.dropdown.Option('4'),
                                                  ft.dropdown.Option('5'), ft.dropdown.Option('6')],
                                         value=str(self.ex_data.get_week_int()),
                                         width=60, height=50, on_change=self.update_week),
                             ft.Text('         WORKOUT  ', size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('A'), ft.dropdown.Option('B'),
                                                  ft.dropdown.Option('C')],
                                         value=str(self.ex_data.get_workout_letter()),
                                         width=60, height=50, on_change=self.update_workout)
                             ]),
        )


class ExerciseView:
    def __init__(self, ex_data: ExerciseData):
        self.ex_data = ex_data
        self.schedule = ex_data.schedule
        self.program = ex_data.program
        self.stage = ex_data.stage
        self.week = ex_data.week
        self.workout = ex_data.workout
        self.circuit = ex_data.circuit
        self.exercise_index = ex_data.exercise_index

        self.exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

    def get_image(self) -> ft.Image:
        name = self.exercises['name'][self.exercise_index]
        name = name.replace(' ', '_').lower()
        name = name.replace(' ', '_').lower()
        file = f"exercise_pics/{name}.png"
        if not os.path.isfile(os.path.join(os.getenv("FLET_ASSETS_DIR"), file)):
            file = f"assets/exercise_pics/no_pic.png"

        img = ft.Image(
            src=file,
            width=100,
            height=60,
            fit=ft.ImageFit.CONTAIN,
        )
        return img
    
    def get_name_text(self) -> ft.Text:
        name = self.exercises['name'][self.exercise_index]
        words_in_name = name.split(' ')
        name = ''
        for i, word in enumerate(words_in_name):
            name += word + ' '
            if i != 0 and (i - 1) % 3 == 0:
                name += '\n'
    
        name_font_size = 20 #if len(words_in_name) < 6 else 16
    
        ex_name = ft.Text(f"{name.upper()}", size=name_font_size, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
    
        return ex_name
    
    def generate_name_row(self) -> ft.Row:
        img = self.get_image()
        ex_name = self.get_name_text()
        exercise_name_row = ft.Row(expand=0, wrap=False)
        exercise_name_row.controls.append(img)
        exercise_name_row.controls.append(ex_name)
    
        return exercise_name_row
    
    def get_stats_names_column(self, stats_column_height: int, stats_font_size: int) -> ft.Column:
        stats_column_names = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)
        warmup_sets = ft.Text(f"WARMUP SETS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                              color=ft.Colors.BLACK)
        warmup_reps = ft.Text(f"WARMUP REPS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                              color=ft.Colors.BLACK)
        work_sets = ft.Text(f"WORK SETS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK)
        work_reps = ft.Text(f"WORK REPS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK)
        tempo = ft.Text(f"TEMPO: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK)
        rest = ft.Text(f"REST: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                       color=ft.Colors.BLACK)
        stats_column_names.controls.append(warmup_sets)
        stats_column_names.controls.append(warmup_reps)
        stats_column_names.controls.append(work_sets)
        stats_column_names.controls.append(work_reps)
        stats_column_names.controls.append(tempo)
        stats_column_names.controls.append(rest)
    
        return stats_column_names
    
    def get_stats_values_column(self, stats_column_height: int, stats_font_size: int) -> ft.Column:
        stats_column_values = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)
        ex_warmup_sets_value = ' ' if len(self.exercises['warmup sets']) == 0 else self.exercises['warmup sets'][
            self.exercise_index].upper()
        ex_warmup_sets = ft.Text(f"{ex_warmup_sets_value}", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLACK)
        ex_warmup_reps_value = ' ' if len(self.exercises['warmup sets']) == 0 else self.exercises['warmup sets'][
            self.exercise_index].upper()
        ex_warmup_reps = ft.Text(f"{ex_warmup_reps_value}", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLACK)
        ex_work_sets = ft.Text(f"{self.exercises['work sets'][self.exercise_index].upper()}", size=stats_font_size,
                               weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        ex_work_reps = ft.Text(f"{self.exercises['work reps'][self.exercise_index].upper()}", size=stats_font_size,
                               weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        ex_tempo = ft.Text(f"{self.exercises['tempo'][self.exercise_index].upper()}", size=stats_font_size,
                           weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        ex_rest = ft.Text(f"{self.exercises['rest'][self.exercise_index].upper()}", size=stats_font_size,
                          weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        stats_column_values.controls.append(ex_warmup_sets)
        stats_column_values.controls.append(ex_warmup_reps)
        stats_column_values.controls.append(ex_work_sets)
        stats_column_values.controls.append(ex_work_reps)
        stats_column_values.controls.append(ex_tempo)
        stats_column_values.controls.append(ex_rest)
    
        return stats_column_values
    
    def generate_stats(self, row_width: int, stats_column_height: int, stats_font_size: int) -> ft.Row:
        stats_row = ft.Row(width=row_width)
    
        stats_column_names = self.get_stats_names_column(stats_column_height, stats_font_size)
        stats_column_values = self.get_stats_values_column(stats_column_height, stats_font_size)
        stats_row.controls.append(stats_column_names)
        stats_row.controls.append(stats_column_values)
    
        return stats_row

    def generate_circuit_number_input_column(self, stats_font_size: int) -> ft.Column:
        circuits_text = ft.Text("EXERCISES ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLACK)

        work_reps = self.exercises['work sets'][self.exercise_index]
        warmup_reps = 0 if len(self.exercises['warmup sets']) == 0 else int(self.exercises['warmup sets'][
            self.exercise_index])
        num_of_reps = int(work_reps) + int(warmup_reps)
        controls = [circuits_text]
        for c in range(num_of_reps):
            circuit = ft.Text(f'WARMUP {c + 1}', weight=ft.FontWeight.BOLD) if c < warmup_reps else \
                ft.Text(f'WORK {c + 1 - warmup_reps}', weight=ft.FontWeight.BOLD)
            controls.append(circuit)

        circuit_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return circuit_column

    def generate_reps_input_column(self, stats_row: ft.Row, stats_font_size: int) -> ft.Column:
    
        reps_text = ft.Text("REPS ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK)

        def update_schedule(e):
            work = True if e.control.data[1] == 'work' else False
            if work:
                self.exercises['work reps done'][self.exercise_index][e.control.data[0]] = e.control.value
            else:
                self.exercises['warmup reps done'][self.exercise_index][e.control.data[0]] = e.control.value
            self.ex_data.save()

        work_reps = self.exercises['work sets'][self.exercise_index]
        warmup_reps = 0 if len(self.exercises['warmup sets']) == 0 else int(self.exercises['warmup sets'][self.exercise_index])
        num_of_reps = int(work_reps) + int(warmup_reps)
        controls = [reps_text]
        for c in range(num_of_reps):
            work_or_warmup = 'warmup' if c < warmup_reps else 'work'
            reps = []
            for i in stats_row.controls[1].controls[3].value.split('-'):
                if i != 'MAX':
                    reps.append(int(i))
                else:
                    reps.append(1)
                    reps.append(40)

            reps_input_options = [ft.dropdown.Option(f'{i}') for i in range(reps[0], reps[1] + 1)] if len(reps) > 1 \
                else [ft.dropdown.Option(f'{reps[0]}')]
            reps_input = ft.Dropdown(width=60, height=45, options=reps_input_options, on_change=update_schedule,
                                     data=[c, work_or_warmup])
            reps_input.value = self.exercises['work reps done'][self.exercise_index][c - warmup_reps] if work_or_warmup == 'work' \
                else self.exercises['warmup reps done'][self.exercise_index][c]
            controls.append(reps_input)

        reps_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return reps_column

    def generate_kilos_input_column(self, stats_font_size: int) -> ft.Column:
        kilos_text = ft.Text("KILOS", size=stats_font_size, weight=ft.FontWeight.BOLD,
                             color=ft.Colors.BLACK)

        def update_schedule(e):
            work = True if e.control.data[1] == 'work' else False
            if work:
                self.exercises['work kilos done'][self.exercise_index][e.control.data[0]] = e.control.value
            else:
                self.exercises['warmup kilos done'][self.exercise_index][e.control.data[0]] = e.control.value
            self.ex_data.save()

        work_reps = self.exercises['work sets'][self.exercise_index]
        warmup_reps = 0 if len(self.exercises['warmup sets']) == 0 else int(self.exercises['warmup sets'][
            self.exercise_index])
        num_of_reps = int(work_reps) + int(warmup_reps)
        controls = [kilos_text]
        for c in range(num_of_reps):
            work_or_warmup = 'warmup' if c < warmup_reps else 'work'
            kilos_units_input_options = [ft.dropdown.Option(f'{i}') for i in range(200)]
            kilos_units_input = ft.Dropdown(width=100, height=45, options=kilos_units_input_options,
                                            on_change=update_schedule, data=[c, work_or_warmup])
            kilos_units_input.value = self.exercises['work kilos done'][self.exercise_index][c - warmup_reps] if work_or_warmup == 'work' \
                else self.exercises['warmup kilos done'][self.exercise_index][c]
            controls.append(kilos_units_input)
    
        kilos_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return kilos_column
    
    def generate_input_row(self, stats_row: ft.Row, stats_font_size: int, row_width: int) -> ft.Row:
        inputs_row = ft.Row(width=row_width * 2)

        circuits_column = self.generate_circuit_number_input_column(stats_font_size)
        reps_column = self.generate_reps_input_column(stats_row, stats_font_size)
        kilos_column = self.generate_kilos_input_column(stats_font_size)
        inputs_row.controls.append(circuits_column)
        inputs_row.controls.append(reps_column)
        inputs_row.controls.append(kilos_column)
    
        return inputs_row
    
    def generate_view(self, page: ft.Page):
        stats_row_width = 150
        stats_column_height = 120
        stats_font_size = 16

        exercise_name_row = self.generate_name_row()
    
        stats_row = self.generate_stats(row_width=stats_row_width, stats_column_height=stats_column_height,
                                        stats_font_size=stats_font_size)
        inputs_row = self.generate_input_row(stats_row, stats_font_size, stats_row_width)

        page.add(ft.Row(controls=[
            ft.Text(f"CIRCUIT {int(self.circuit.split(' ')[1])}", size=20, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE),
            ft.Text(f"EXERCISE {self.exercise_index + 1}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
            ]))
        page.add(exercise_name_row)
        page.add(stats_row)
        page.add(ft.Divider(height=20, color="white"))
        page.add(inputs_row)


class NavigationButtonsView:
    def __init__(self, ex_data: ExerciseData, previous_ex: Callable, next_ex: Callable,
                 previous_circ: Callable, next_circ: Callable):
        self.ex_data = ex_data
        self.schedule = ex_data.schedule
        self.program = ex_data.program
        self.stage = ex_data.stage
        self.week = ex_data.week
        self.workout = ex_data.workout
        self.circuit = ex_data.circuit
        self.exercise_index = ex_data.exercise_index

        self.exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

        self.previous_ex = previous_ex
        self.next_ex = next_ex
        self.previous_circ = previous_circ
        self.next_circ = next_circ

    def generate_view(self, page):
        back_ex_button = ft.FilledTonalButton(content=ft.Row([ft.Icon(ft.Icons.NAVIGATE_BEFORE, size=20),
                                                              ft.Text('   Previous\n   Exercise')]),
                                              on_click=self.previous_ex)
        front_ex_button = ft.FilledTonalButton(content=ft.Row([ft.Text('   Next   \n   Exercise'),
                                                           ft.Icon(ft.Icons.NAVIGATE_NEXT, size=20)],
                                                           spacing=1),
                                            on_click=self.next_ex)

        back_circ_button = ft.FilledTonalButton(content=ft.Row([ft.Icon(ft.Icons.SKIP_PREVIOUS, size=20),
                                                            ft.Text('     Previous\n     Circuit  ')],
                                                            spacing=1),
                                             on_click=self.previous_circ)
        front_circ_button = ft.FilledTonalButton(content=ft.Row([ft.Text('   Next   \n   Circuit  '),
                                                              ft.Icon(ft.Icons.SKIP_NEXT, size=20)],
                                                             spacing=1),
                                              on_click=self.next_circ)

        page.add(ft.Divider(height=20, color='white'))
        page.add(ft.Row(controls=[back_ex_button, front_ex_button]))
        page.add(ft.Row(controls=[back_circ_button, front_circ_button]))