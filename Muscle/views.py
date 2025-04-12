from typing import Callable, Tuple

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
            ft.Text('                 ', visible=True, height=20),
            ft.Row(controls=[ft.Text('PROGRAM ', size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('beginner'), ft.dropdown.Option('intermediate'),
                                                  ft.dropdown.Option('advanced')],
                                         value=str(self.ex_data.program), dense=True, select_icon_size=1,
                                         width=90, height=35, on_change=self.update_program, text_size=15,
                                         content_padding=10),
                             ft.Text('STAGE       ', size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('1'), ft.dropdown.Option('2'),
                                                  ft.dropdown.Option('3'), ft.dropdown.Option('4')],
                                         value=str(self.ex_data.get_stage_int()),
                                         width=60, height=35, on_change=self.update_stage, text_size=15,
                                         content_padding=10)],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row(controls=[ft.Text('WEEK        ', size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('1'), ft.dropdown.Option('2'),
                                                  ft.dropdown.Option('3'), ft.dropdown.Option('4'),
                                                  ft.dropdown.Option('5'), ft.dropdown.Option('6')],
                                         value=str(self.ex_data.get_week_int()),
                                         width=60, height=35, on_change=self.update_week, text_size=15,
                                         content_padding=10),
                             ft.Text('     WORKOUT', size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                             ft.Dropdown(options=[ft.dropdown.Option('1'), ft.dropdown.Option('2'),
                                                  ft.dropdown.Option('3')],
                                         value=str(self.ex_data.get_workout_int()),
                                         width=60, height=35, on_change=self.update_workout, text_size=15,
                                         content_padding=10)],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        )


class ExerciseView:
    def __init__(self, ex_data: ExerciseData, on_done: Callable):
        self.ex_data = ex_data
        self.schedule = ex_data.schedule
        self.program = ex_data.program
        self.stage = ex_data.stage
        self.week = ex_data.week
        self.workout = ex_data.workout
        self.circuit = ex_data.circuit
        self.exercise_index = ex_data.exercise_index

        self.exercises = self.schedule[self.program][self.stage][self.week][self.workout][self.circuit]

        self.on_done = on_done

    def generate_exercise_info_row(self) -> ft.Row:
        now = f'{self.exercises["work sets done"][self.exercise_index]}'
        if now != '0':
            now = now.split(' ')
            now[1] = now[1].split('.')[0]
            now = f'{now[0]}\n{now[1]}'
        on_done_text = ft.Text(now)

        exercise_info_row = ft.Row(controls=[
            ft.Column(
                controls=[ft.Text(f"CIRCUIT {int(self.circuit.split(' ')[1])}", size=15, weight=ft.FontWeight.BOLD,
                                  color=ft.Colors.BLUE),
                          ft.Text(f"EXERCISE {self.exercise_index + 1}", size=15, weight=ft.FontWeight.BOLD,
                                  color=ft.Colors.BLUE)]),
            ft.Column(
                controls=[ft.FilledTonalButton(content=ft.Text("DONE ON"), width=100, on_click=self.on_done,
                                               data=on_done_text),
                          on_done_text]
            )],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return exercise_info_row

    def get_image(self) -> ft.Image:
        name = self.exercises['name'][self.exercise_index]
        name = name.replace(' ', '_').lower()
        name = name.replace(' ', '_').lower()
        file = f"exercise_pics/{name}.png"

        img = ft.Image(
            src=file,
            width=100,
            height=60,
            fit=ft.ImageFit.FILL,
        )

        return img
    
    def get_name_text(self) -> ft.Text:
        name = self.exercises['name'][self.exercise_index]
        name_font_size = 16  # if len(words_in_name) < 6 else 14
    
        ex_name = ft.Text(f"{name.upper()}", size=name_font_size, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE,
                          width=200, height=70)
    
        return ex_name
    
    def generate_name_row(self) -> ft.Row:
        img = self.get_image()
        ex_name = self.get_name_text()
        exercise_name_row = ft.Row()
        exercise_name_row.controls.append(img)
        exercise_name_row.controls.append(ex_name)
    
        return exercise_name_row
    
    def get_stats_names_columns(self, stats_column_height: int, stats_font_size: int) -> Tuple[ft.Column, ft.Column]:
        stats_column_names_left = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)
        stats_column_names_right = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)
        warmup_sets = ft.Text(f"WARMUP SETS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                              color=ft.Colors.BLUE)
        warmup_reps = ft.Text(f"WARMUP REPS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                              color=ft.Colors.BLUE)
        work_sets = ft.Text(f"WORK SETS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE)
        work_reps = ft.Text(f"WORK REPS: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE)
        tempo = ft.Text(f"TEMPO: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE)
        rest = ft.Text(f"REST: ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                       color=ft.Colors.BLUE)
        stats_column_names_left.controls.append(warmup_sets)
        stats_column_names_left.controls.append(warmup_reps)
        stats_column_names_left.controls.append(work_sets)
        stats_column_names_right.controls.append(work_reps)
        stats_column_names_right.controls.append(tempo)
        stats_column_names_right.controls.append(rest)
    
        return stats_column_names_left, stats_column_names_right
    
    def get_stats_values_columns(self, stats_column_height: int, stats_font_size: int) -> Tuple[ft.Column, ft.Column]:
        stats_column_values_left = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)
        stats_column_values_right = ft.Column(alignment=ft.MainAxisAlignment.SPACE_AROUND, height=stats_column_height)

        ex_warmup_sets_value = ' ' if len(self.exercises['warmup sets']) == 0 else self.exercises['warmup sets'][
            self.exercise_index].upper()
        ex_warmup_sets = ft.Text(f"{ex_warmup_sets_value}", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLUE)
        ex_warmup_reps_value = ' ' if len(self.exercises['warmup sets']) == 0 else self.exercises['warmup sets'][
            self.exercise_index].upper()
        ex_warmup_reps = ft.Text(f"{ex_warmup_reps_value}", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLUE)
        ex_work_sets = ft.Text(f"{self.exercises['work sets'][self.exercise_index].upper()}", size=stats_font_size,
                               weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        ex_work_reps = ft.Text(f"{self.exercises['work reps'][self.exercise_index].upper()}", size=stats_font_size,
                               weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        ex_tempo = ft.Text(f"{self.exercises['tempo'][self.exercise_index].upper()}", size=stats_font_size,
                           weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        ex_rest = ft.Text(f"{self.exercises['rest'][self.exercise_index].upper()}", size=stats_font_size,
                          weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)

        stats_column_values_left.controls.append(ex_warmup_sets)
        stats_column_values_left.controls.append(ex_warmup_reps)
        stats_column_values_left.controls.append(ex_work_sets)
        stats_column_values_right.controls.append(ex_work_reps)
        stats_column_values_right.controls.append(ex_tempo)
        stats_column_values_right.controls.append(ex_rest)
    
        return stats_column_values_left, stats_column_values_right
    
    def generate_stats(self, row_width: int, stats_column_height: int, stats_font_size: int) -> ft.Row:
        stats_row = ft.Row(width=row_width)
    
        stats_column_names_left, stats_column_names_right = self.get_stats_names_columns(stats_column_height, stats_font_size)
        stats_column_values_left, stats_column_values_right = self.get_stats_values_columns(stats_column_height, stats_font_size)
        stats_row.controls.append(stats_column_names_left)
        stats_row.controls.append(stats_column_values_left)
        stats_row.controls.append(ft.VerticalDivider(width=80, color='white'))
        stats_row.controls.append(stats_column_names_right)
        stats_row.controls.append(stats_column_values_right)
    
        return stats_row

    def generate_circuit_number_input_column(self, stats_font_size: int) -> ft.Column:
        circuits_text = ft.Text("EXERCISES ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                                 color=ft.Colors.BLUE)

        work_reps = self.exercises['work sets'][self.exercise_index]
        warmup_reps = 0 if len(self.exercises['warmup sets']) == 0 else int(self.exercises['warmup sets'][
            self.exercise_index])
        num_of_reps = int(work_reps) + int(warmup_reps)
        controls = [circuits_text]
        for c in range(num_of_reps):
            circuit = ft.Text(f'WARMUP {c + 1}', weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE) if c < warmup_reps \
                else ft.Text(f'WORK {c + 1 - warmup_reps}', weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
            controls.append(circuit)

        circuit_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return circuit_column

    def generate_reps_input_column(self, stats_row: ft.Row, stats_font_size: int) -> ft.Column:
    
        reps_text = ft.Text("REPS ", size=stats_font_size, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE)

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
            for i in stats_row.controls[4].controls[0].value.split('-'):
                if i != 'MAX':
                    reps.append(int(i))
                else:
                    reps.append(1)
                    reps.append(40)

            reps_input_options = [ft.dropdown.Option(f'{i}') for i in range(reps[0] - 2, reps[1] + 1)] if len(reps) > 1 \
                else [ft.dropdown.Option(f'{reps[0] - 2}'), ft.dropdown.Option(f'{reps[0] - 1}'), ft.dropdown.Option(f'{reps[0]}')]
            reps_input = ft.Dropdown(width=60, height=45, options=reps_input_options, on_change=update_schedule,
                                     data=[c, work_or_warmup], text_size=14)
            reps_input.value = self.exercises['work reps done'][self.exercise_index][c - warmup_reps] if work_or_warmup == 'work' \
                else self.exercises['warmup reps done'][self.exercise_index][c]
            controls.append(reps_input)

        reps_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return reps_column

    def generate_kilos_input_column(self, stats_font_size: int) -> ft.Column:
        kilos_text = ft.Text("KILOS", size=stats_font_size, weight=ft.FontWeight.BOLD,
                             color=ft.Colors.BLUE)

        def update_schedule(e):
            work_type = 'work kilos done' if e.control.data[1] == 'work' else 'warmup kilos done'
            is_decimal = e.control.data[2]

            current_kilos = float(self.exercises[work_type][self.exercise_index][e.control.data[0]])
            int_kilos = int(current_kilos)
            decimal_kilos = current_kilos - int(current_kilos)

            if is_decimal:
                decimal_kilos = float(e.control.value)
            else:
                int_kilos = float(e.control.value)

            new_kilos = str(int_kilos + decimal_kilos)

            self.exercises[work_type][self.exercise_index][e.control.data[0]] = new_kilos
            self.ex_data.save()

        work_reps = self.exercises['work sets'][self.exercise_index]
        warmup_reps = 0 if len(self.exercises['warmup sets']) == 0 else int(self.exercises['warmup sets'][
            self.exercise_index])
        num_of_reps = int(work_reps) + int(warmup_reps)
        controls = [kilos_text]
        for c in range(num_of_reps):
            work_or_warmup = 'warmup' if c < warmup_reps else 'work'
            full_kilos_units_input_options = [ft.dropdown.Option(f'{i}') for i in range(200)]
            full_kilos_units_input = ft.Dropdown(width=55, height=45, options=full_kilos_units_input_options,
                                                 on_change=update_schedule, data=[c, work_or_warmup, False], text_size=14)

            decimal_kilos_input_options = [ft.dropdown.Option(f'{i}') for i in [x/10 for x in range(10)]]
            decimal_kilos_units_input = ft.Dropdown(width=45, height=45, options=decimal_kilos_input_options,
                                                    on_change=update_schedule, data=[c, work_or_warmup, True], text_size=10)

            current_kilos_value = self.exercises['work kilos done'][self.exercise_index][c - warmup_reps] if work_or_warmup == 'work' \
                else self.exercises['warmup kilos done'][self.exercise_index][c]
            full_kilos_current_value = int(float(current_kilos_value))
            decimal_kilos_current_value = (round((float(current_kilos_value) - full_kilos_current_value)*10))/10
            full_kilos_units_input.value = str(full_kilos_current_value)
            decimal_kilos_units_input.value = str(decimal_kilos_current_value)
            both_full_and_decimal = ft.Row(controls=[full_kilos_units_input, decimal_kilos_units_input])
            controls.append(both_full_and_decimal)
    
        kilos_column = ft.Column(controls=controls, height=50 * num_of_reps, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return kilos_column
    
    def generate_input_row(self, stats_row: ft.Row, stats_font_size: int, row_width: int) -> ft.Row:
        inputs_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        circuits_column = self.generate_circuit_number_input_column(stats_font_size)
        reps_column = self.generate_reps_input_column(stats_row, stats_font_size)
        kilos_column = self.generate_kilos_input_column(stats_font_size)
        inputs_row.controls.append(circuits_column)
        inputs_row.controls.append(reps_column)
        inputs_row.controls.append(kilos_column)
    
        return inputs_row
    
    def generate_view(self, page: ft.Page):
        stats_row_width = 150
        stats_column_height = 50
        stats_font_size = 14

        exercise_info_row = self.generate_exercise_info_row()

        exercise_name_row = self.generate_name_row()
    
        stats_row = self.generate_stats(row_width=stats_row_width, stats_column_height=stats_column_height,
                                        stats_font_size=stats_font_size)
        inputs_row = self.generate_input_row(stats_row, stats_font_size, stats_row_width)

        page.add(exercise_info_row)
        page.add(exercise_name_row)
        page.add(stats_row)
        page.add(inputs_row)


class NavigationButtonsView:
    def __init__(self, ex_data: ExerciseData, previous_ex: Callable, next_ex: Callable,
                 previous_circ: Callable, next_circ: Callable, send_email: Callable):
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
        self.send_email = send_email

    def generate_view(self, page):
        back_ex_button = ft.FilledTonalButton(content=ft.Row([ft.Icon(ft.Icons.NAVIGATE_BEFORE, size=20),
                                                              ft.Text('   Previous\n   Exercise')]),
                                              on_click=self.previous_ex, width=130)
        front_ex_button = ft.FilledTonalButton(content=ft.Row([ft.Text('   Next   \n   Exercise'),
                                                               ft.Icon(ft.Icons.NAVIGATE_NEXT, size=20)],
                                                              spacing=20),
                                               on_click=self.next_ex, width=130)

        back_circ_button = ft.FilledTonalButton(content=ft.Row([ft.Icon(ft.Icons.SKIP_PREVIOUS, size=20),
                                                                ft.Text('     Previous\n     Circuit  ')],
                                                               spacing=1),
                                                on_click=self.previous_circ, width=130)
        front_circ_button = ft.FilledTonalButton(content=ft.Row([ft.Text('   Next   \n   Circuit  '),
                                                                 ft.Icon(ft.Icons.SKIP_NEXT, size=20)],
                                                                spacing=20),
                                                 on_click=self.next_circ, width=130)
        email_button = ft.FilledTonalButton(content=ft.Text('Send schedule by email'),
                                            on_click=self.send_email, width=130)

        page.add(ft.Divider(height=10, color='white'))
        page.add(ft.Row(controls=[back_ex_button, front_ex_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        page.add(ft.Row(controls=[back_circ_button, front_circ_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        page.add(email_button)
