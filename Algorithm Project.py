import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random  # For generating test arrays easily
import time    # yield will mostly control speed

# --- Color Of Visualization ---
BAR_COLOR_DEFAULT = "skyblue"
BAR_COLOR_COMPARE = "orangered"  # Elements being actively compared
BAR_COLOR_SWAP = "gold"          # Elements being swapped
BAR_COLOR_PIVOT = "magenta"      # Pivot element in Quick Sort
BAR_COLOR_KEY = "purple"         # Key element in Insertion Sort
BAR_COLOR_SORTED_SECTION = "lightgreen"    # Part of array known to be sorted
BAR_COLOR_FINAL_POSITION = "forestgreen"   # Element placed in its final sorted position
BAR_COLOR_SUBARRAY = "lightgrey"           # For Merge Sort sub-array indication
BAR_COLOR_FOCUS = "cyan"                   # General focus for merge sort elements


# --- Sorting Algorithm Visualizations ---
def insertion_sort_visual(app_ref):
    
    array = list(app_ref.array_data) # Work on a copy of the app's current data
    n = len(array)
    if n == 0: # Handle empty array case
        app_ref.update_display_direct([], {})
        yield
        return
    if n == 1:
        app_ref.update_display_direct(array, {0: BAR_COLOR_SORTED_SECTION})
        yield
        return

    # Initially mark first element as sorted_section
    app_ref.update_display_direct(array, {0: BAR_COLOR_SORTED_SECTION})
    yield # Initial display

    for i in range(1, n):
        key = array[i]
        j = i - 1
        
        colors = {k: BAR_COLOR_SORTED_SECTION for k in range(i)}
        colors[i] = BAR_COLOR_KEY
        if j >= 0: colors[j] = BAR_COLOR_COMPARE
        app_ref.update_display_direct(array, colors)
        yield
        
        while j >= 0 and key < array[j]:
            colors = {k: BAR_COLOR_SORTED_SECTION for k in range(i)}
            colors[i] = BAR_COLOR_KEY
            colors[j] = BAR_COLOR_COMPARE
            colors[j+1] = BAR_COLOR_COMPARE
            app_ref.update_display_direct(array, colors)
            yield

            array[j + 1] = array[j]
            
            colors[j + 1] = BAR_COLOR_SWAP
            colors[j] = BAR_COLOR_SORTED_SECTION 
            app_ref.update_display_direct(array, colors)
            yield
            
            j -= 1
            
            if j >= 0:
                colors = {k: BAR_COLOR_SORTED_SECTION for k in range(i)}
                colors[i] = BAR_COLOR_KEY
                colors[j] = BAR_COLOR_COMPARE
                app_ref.update_display_direct(array, colors)
                yield

        array[j + 1] = key
        
        colors = {k: BAR_COLOR_SORTED_SECTION for k in range(i + 1)}
        colors[j + 1] = BAR_COLOR_FINAL_POSITION
        app_ref.update_display_direct(array, colors)
        yield
        
        colors[j + 1] = BAR_COLOR_SORTED_SECTION
        app_ref.update_display_direct(array, colors)
        yield

    app_ref.update_display_direct(array, {k: BAR_COLOR_SORTED_SECTION for k in range(n)})
    app_ref.array_data = array
    yield


# --- Merge Algorithm Visualizations ---
def merge_sort_visual(app_ref):
    
    array = list(app_ref.array_data)
    n = len(array)
    if n == 0: # Handle empty array case
        app_ref.update_display_direct([], {})
        yield
        return
    if n == 1:
        app_ref.update_display_direct(array, {0: BAR_COLOR_SORTED_SECTION})
        yield
        return

    yield from _merge_sort_recursive_visual(array, 0, n - 1, app_ref)
    
    app_ref.update_display_direct(array, {k: BAR_COLOR_SORTED_SECTION for k in range(n)})
    app_ref.array_data = array
    yield

def _merge_sort_recursive_visual(array, l_idx, r_idx, app_ref):
    if l_idx < r_idx:
        m_idx = l_idx + (r_idx - l_idx) // 2
        
        colors = {i: BAR_COLOR_SUBARRAY if l_idx <= i <= r_idx else BAR_COLOR_DEFAULT for i in range(len(array))}
        app_ref.update_display_direct(array, colors)
        yield

        yield from _merge_sort_recursive_visual(array, l_idx, m_idx, app_ref)
        yield from _merge_sort_recursive_visual(array, m_idx + 1, r_idx, app_ref)
        yield from _merge_visual(array, l_idx, m_idx, r_idx, app_ref)

def _merge_visual(array, l_orig, m_orig, r_orig, app_ref):
    n1 = m_orig - l_orig + 1
    n2 = r_orig - m_orig

    L_temp = [array[l_orig + i] for i in range(n1)]
    R_temp = [array[m_orig + 1 + j] for j in range(n2)]

    i_temp, j_temp, k_orig = 0, 0, l_orig

    while i_temp < n1 and j_temp < n2:
        colors = {idx: (BAR_COLOR_SORTED_SECTION if idx < l_orig or idx > r_orig else BAR_COLOR_SUBARRAY) for idx in range(len(array))}
        colors[l_orig + i_temp] = BAR_COLOR_COMPARE
        colors[m_orig + 1 + j_temp] = BAR_COLOR_COMPARE
        app_ref.update_display_direct(array, colors)
        yield

        if L_temp[i_temp] <= R_temp[j_temp]:
            array[k_orig] = L_temp[i_temp]
            colors[k_orig] = BAR_COLOR_SWAP
            app_ref.update_display_direct(array, colors)
            yield
            colors[k_orig] = BAR_COLOR_FOCUS
            i_temp += 1
        else:
            array[k_orig] = R_temp[j_temp]
            colors[k_orig] = BAR_COLOR_SWAP
            app_ref.update_display_direct(array, colors)
            yield
            colors[k_orig] = BAR_COLOR_FOCUS
            j_temp += 1
        k_orig += 1
    
    while i_temp < n1:
        colors = {idx: (BAR_COLOR_SORTED_SECTION if idx < l_orig or idx > r_orig else BAR_COLOR_SUBARRAY) for idx in range(len(array))}
        colors[l_orig + i_temp] = BAR_COLOR_COMPARE
        array[k_orig] = L_temp[i_temp]
        colors[k_orig] = BAR_COLOR_SWAP
        app_ref.update_display_direct(array, colors)
        yield
        colors[k_orig] = BAR_COLOR_FOCUS
        i_temp += 1
        k_orig += 1

    while j_temp < n2:
        colors = {idx: (BAR_COLOR_SORTED_SECTION if idx < l_orig or idx > r_orig else BAR_COLOR_SUBARRAY) for idx in range(len(array))}
        colors[m_orig + 1 + j_temp] = BAR_COLOR_COMPARE
        array[k_orig] = R_temp[j_temp]
        colors[k_orig] = BAR_COLOR_SWAP
        app_ref.update_display_direct(array, colors)
        yield
        colors[k_orig] = BAR_COLOR_FOCUS
        j_temp += 1
        k_orig += 1

    final_range_colors = {idx: BAR_COLOR_DEFAULT for idx in range(len(array))}
    for idx_sorted in range(l_orig, r_orig + 1):
        final_range_colors[idx_sorted] = BAR_COLOR_SORTED_SECTION
    app_ref.update_display_direct(array, final_range_colors)
    yield


# --- Quick Algorithm Visualizations ---
def quick_sort_visual(app_ref):
    
    array = list(app_ref.array_data)
    n = len(array)
    if n == 0: # Handle empty array case
        app_ref.update_display_direct([], {})
        yield
        return
    if n == 1:
        app_ref.update_display_direct(array, {0: BAR_COLOR_SORTED_SECTION})
        yield
        return

    yield from _quick_sort_recursive_visual(array, 0, n - 1, app_ref)
    
    app_ref.update_display_direct(array, {k: BAR_COLOR_SORTED_SECTION for k in range(n)})
    app_ref.array_data = array
    yield

def _quick_sort_recursive_visual(array, low, high, app_ref):
    if low < high:
        colors = {i: (BAR_COLOR_SUBARRAY if low <= i <= high else BAR_COLOR_DEFAULT) for i in range(len(array))}
        app_ref.update_display_direct(array, colors)
        yield
        
        partition_generator = _partition_visual(array, low, high, app_ref)
        pi = None
        while True:
            try:
                val = next(partition_generator)
                if isinstance(val, int): 
                    pi = val
                yield 
            except StopIteration:
                break
        
        if pi is None: 
            for idx_check in range(low, high + 1):
                if app_ref.last_color_info.get(idx_check) == BAR_COLOR_FINAL_POSITION:
                    pi = idx_check
                    break
            if pi is None:
                print(f"ERROR: Pivot index not found after partition for range {low}-{high}")
                return 


        app_ref.update_display_direct(array, {pi: BAR_COLOR_FINAL_POSITION})
        yield

        yield from _quick_sort_recursive_visual(array, low, pi - 1, app_ref)
        yield from _quick_sort_recursive_visual(array, pi + 1, high, app_ref)
        
        colors = {i: BAR_COLOR_SORTED_SECTION for i in range(low, high + 1)}
        app_ref.update_display_direct(array, colors, True)
        yield

def _partition_visual(array, low, high, app_ref):
    pivot_val = array[high]
    i_ptr = low - 1

    colors = {k: (BAR_COLOR_SUBARRAY if low <= k < high else BAR_COLOR_DEFAULT) for k in range(len(array))}
    colors[high] = BAR_COLOR_PIVOT
    app_ref.update_display_direct(array, colors)
    yield

    for j_ptr in range(low, high):
        colors[j_ptr] = BAR_COLOR_COMPARE
        if i_ptr >= low : colors[i_ptr] = BAR_COLOR_FOCUS
        app_ref.update_display_direct(array, colors)
        yield

        if array[j_ptr] <= pivot_val:
            i_ptr += 1
            array[i_ptr], array[j_ptr] = array[j_ptr], array[i_ptr]
            
            temp_colors = colors.copy()
            temp_colors[i_ptr] = BAR_COLOR_SWAP
            temp_colors[j_ptr] = BAR_COLOR_SWAP
            app_ref.update_display_direct(array, temp_colors)
            yield
        
        colors[j_ptr] = BAR_COLOR_SUBARRAY if low <= j_ptr < high else BAR_COLOR_DEFAULT
        if i_ptr >=low : colors[i_ptr] = BAR_COLOR_FOCUS

    final_pivot_idx = i_ptr + 1
    array[final_pivot_idx], array[high] = array[high], array[final_pivot_idx]
    
    colors = {k: BAR_COLOR_DEFAULT for k in range(len(array))}
    for k_range in range(low, high+1): colors[k_range] = BAR_COLOR_SUBARRAY
    colors[final_pivot_idx] = BAR_COLOR_SWAP
    colors[high] = BAR_COLOR_SWAP
    app_ref.update_display_direct(array, colors)
    yield
    
    colors[final_pivot_idx] = BAR_COLOR_FINAL_POSITION
    if high in colors and high != final_pivot_idx: colors[high] = BAR_COLOR_SUBARRAY
    app_ref.update_display_direct(array, colors)
    yield

    yield final_pivot_idx


# --- GUI Application ---
class SortingApp:
    def __init__(self, master):
        self.master = master
        master.title("Sorting Algorithm Visualizer")
        master.geometry("850x750")

        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            print("Clam theme not available, using default.")
            self.style.theme_use('default')

        self.style.configure("Rounded.TButton", padding=6, relief="flat", font=('Helvetica', 10, 'bold'))
        self.style.configure("TLabel", font=('Helvetica', 10))
        self.style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))

        self.array_data = [] # Initialize as empty
        self.current_generator = None
        self.animation_id = None
        self.is_sorting = False
        self.last_color_info = {}


        # --- Top Control Frame ---
        control_frame = ttk.Frame(master, padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Numbers (comma-separated):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.array_entry = ttk.Entry(control_frame, width=35, font=('Helvetica',10))
        self.array_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        # self.array_entry.insert(0, "64,34,25,12,22,11,90,5,77,40,55,8") # REMOVED: No default insert

        self.generate_button = ttk.Button(control_frame, text="Generate Random", command=self.generate_random_array, style="Rounded.TButton")
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)
        
        control_frame.columnconfigure(1, weight=1)

        # --- Algorithm Selection & Speed ---
        settings_frame = ttk.Frame(master, padding="10")
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algo_var = tk.StringVar(value="Insertion Sort")
        algorithms = ["Insertion Sort", "Merge Sort", "Quick Sort"]
        self.algo_menu = ttk.Combobox(settings_frame, textvariable=self.algo_var, values=algorithms, state="readonly", width=15, font=('Helvetica',10))
        self.algo_menu.set(algorithms[0])
        self.algo_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(settings_frame, text="Speed (ms delay):").grid(row=0, column=2, padx=(20,5), pady=5, sticky="w")
        self.speed_var = tk.IntVar(value=200)
        self.speed_scale = ttk.Scale(settings_frame, from_=10, to=1000, orient=tk.HORIZONTAL, variable=self.speed_var, length=180)
        self.speed_scale.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.speed_label = ttk.Label(settings_frame, text=f"{self.speed_var.get()} ms")
        self.speed_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.speed_var.trace_add("write", self.update_speed_label)

        settings_frame.columnconfigure(1, weight=0)
        settings_frame.columnconfigure(3, weight=1)

        # --- Action Buttons Frame ---
        action_buttons_frame = ttk.Frame(master, padding="5")
        action_buttons_frame.pack(pady=10)

        self.sort_button = ttk.Button(action_buttons_frame, text="Sort", command=self.start_sorting, style="Rounded.TButton")
        self.sort_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_sorting, style="Rounded.TButton", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = ttk.Button(action_buttons_frame, text="Reset", command=self.reset_visualization, style="Rounded.TButton")
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # --- Canvas for Visualization ---
        self.canvas_frame = ttk.Frame(master, relief="sunken", borderwidth=1)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="ivory")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.master.bind('<Configure>', self.on_resize) 
        # self.generate_random_array() # REMOVED: No initial generation
        self.draw_bars([], {}) # Draw empty canvas initially

    def update_speed_label(self, *args):
        self.speed_label.config(text=f"{self.speed_var.get()} ms")

    def on_resize(self, event=None):
        # Only redraw if there's data; otherwise, it might try to draw an empty array
        # which is handled by the initial draw_bars call or reset.
        if self.array_data or not self.is_sorting : # Redraw if there's data or if not sorting (to clear)
             self.draw_bars(self.array_data, self.last_color_info)

    def generate_random_array(self):
        if self.is_sorting:
            messagebox.showwarning("Busy", "Sorting in progress. Please stop or reset.")
            return
        try:
            num_elements = random.randint(10, 30)
            self.array_data = [random.randint(5, 100) for _ in range(num_elements)]
            self.array_entry.delete(0, tk.END)
            self.array_entry.insert(0, ", ".join(map(str, self.array_data)))
            self.last_color_info = {}
            self.draw_bars(self.array_data, self.last_color_info)
            self.enable_controls()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate array: {e}")

    def parse_input_array(self):
        input_str = self.array_entry.get()
        if not input_str.strip(): # Check if input is empty or just whitespace
            self.array_data = [] # Ensure array_data is cleared
            self.last_color_info = {}
            # messagebox.showwarning("Input Error", "Please enter numbers or generate an array.")
            return True # Allow empty input for clearing visualization

        try:
            str_elements = [s.strip() for s in input_str.split(',') if s.strip()]
            if not str_elements: # If after stripping, list is empty
                self.array_data = []
                self.last_color_info = {}
                return True # Allow this state for clearing

            num_array = []
            for s_elem in str_elements:
                try:
                    num_array.append(int(s_elem)) # Assuming integer inputs for simplicity of visualization
                except ValueError:
                     messagebox.showerror("Input Error", f"Invalid number: '{s_elem}'. Please enter integers separated by commas.")
                     return False

            if any(x < 0 for x in num_array): # Basic check for non-negative, as bar height is tricky for negatives
                messagebox.showerror("Input Error", "Please enter non-negative integers for visualization.")
                return False

            self.array_data = num_array
            self.last_color_info = {}
            return True
        except Exception as e: # Catch any other parsing related errors
            messagebox.showerror("Input Error", f"Error parsing input: {e}")
            self.array_data = [] # Clear data on error
            return False

    def draw_bars(self, array_to_draw, color_info, merge_existing_sorted=False):
        self.canvas.delete("all")
        if not array_to_draw: # If array is empty, canvas remains clear
            self.master.update_idletasks() # Ensure canvas is cleared
            return

        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        
        if canvas_height <= 1 or canvas_width <= 1:
            self.master.after(50, lambda: self.draw_bars(array_to_draw, color_info, merge_existing_sorted))
            return

        num_bars = len(array_to_draw)
        bar_spacing_total = 20 
        bar_area_width = canvas_width - bar_spacing_total
        
        bar_width_plus_gap = bar_area_width / num_bars if num_bars > 0 else bar_area_width
        bar_gap = bar_width_plus_gap * 0.15 
        actual_bar_width = bar_width_plus_gap - bar_gap
        if actual_bar_width < 1: actual_bar_width = 1

        # Handle case where all elements are 0 to avoid division by zero or no drawing
        if all(v == 0 for v in array_to_draw):
            max_val_for_scale = 1 # Use 1 to draw minimal height bars for zeros
        else:
            max_val_for_scale = max(v for v in array_to_draw if v > 0) if any(v > 0 for v in array_to_draw) else 1
        
        top_padding = 30 
        bottom_padding = 10
        drawable_height = canvas_height - top_padding - bottom_padding
        height_multiplier = drawable_height / max_val_for_scale if max_val_for_scale > 0 else 1

        current_colors = self.last_color_info.copy() if merge_existing_sorted else {}
        current_colors.update(color_info)
        self.last_color_info = current_colors

        for i, val in enumerate(array_to_draw):
            x0 = bar_spacing_total/2 + i * bar_width_plus_gap + bar_gap / 2
            y0 = canvas_height - bottom_padding 
            
            bar_height = val * height_multiplier if val > 0 else 0
            if val == 0: # Draw a minimal line for zero-value bars
                 bar_height = 2 
            elif bar_height < 2 and val > 0: # Ensure non-zero bars are visible
                 bar_height = 2 
            if bar_height > drawable_height : bar_height = drawable_height # Cap height

            x1 = x0 + actual_bar_width
            y1 = y0 - bar_height

            color = current_colors.get(i, BAR_COLOR_DEFAULT)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=1)
            
            text_x = x0 + actual_bar_width / 2
            text_y = y1 - 10 
            if text_y < 10 : text_y = y0 + 10 if bar_height < canvas_height - 20 else y0 - 10 - bar_height + 15


            self.canvas.create_text(text_x, text_y, text=str(val), font=("Helvetica", 8 if num_bars < 40 else 7), anchor="s")
        self.master.update_idletasks()


    def update_display_direct(self, current_array_state, color_info, merge_sorted=False):
        self.array_data = list(current_array_state)
        self.draw_bars(self.array_data, color_info, merge_sorted)

    def start_sorting(self):
        if self.is_sorting:
            return
        if not self.parse_input_array(): # Ensure array_data is populated or handled if empty
            self.draw_bars(self.array_data, {}) # Draw potentially empty/errored state
            return
        
        if not self.array_data: # If parse_input_array resulted in an empty array (validly)
            messagebox.showinfo("Empty Array", "The array is empty. Nothing to sort.")
            return

        self.is_sorting = True
        self.disable_controls()
        
        algo_name = self.algo_var.get()
        if algo_name == "Insertion Sort":
            self.current_generator = insertion_sort_visual(self)
        elif algo_name == "Merge Sort":
            self.current_generator = merge_sort_visual(self)
        elif algo_name == "Quick Sort":
            self.current_generator = quick_sort_visual(self)
        else:
            self.is_sorting = False
            self.enable_controls()
            return
        self.animate_step()

    def animate_step(self):
        if not self.is_sorting or not self.current_generator:
            self.finish_sorting(interrupted=True) 
            return

        try:
            next_val = next(self.current_generator)
            # ... (logic for handling next_val if specific types are yielded, though mostly handled by update_display_direct)

            delay = self.speed_var.get()
            self.animation_id = self.master.after(delay, self.animate_step)
        except StopIteration:
            self.finish_sorting()
        except Exception as e:
            messagebox.showerror("Runtime Error", f"Error during animation: {e}\nArray: {self.array_data}")
            self.finish_sorting(error=True)


    def finish_sorting(self, error=False, interrupted=False):
        self.is_sorting = False
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        
        if not error and not interrupted and self.array_data: # Check if array_data is not empty
             self.draw_bars(self.array_data, {i: BAR_COLOR_SORTED_SECTION for i in range(len(self.array_data))})
             messagebox.showinfo("Complete", "Sorting finished!")
        elif error and self.array_data:
            self.draw_bars(self.array_data, {i: "red" for i in range(len(self.array_data))})
        # If interrupted or array is empty, the display should be as it was left or cleared.
        
        self.enable_controls()
        self.current_generator = None


    def stop_sorting(self):
        if not self.is_sorting:
            return
        self.is_sorting = False 
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        self.finish_sorting(interrupted=True)
        messagebox.showinfo("Stopped", "Sorting process stopped.")


    def reset_visualization(self):
        if self.is_sorting:
            self.stop_sorting() 

        # Clear the entry and internal data, then redraw empty
        self.array_entry.delete(0, tk.END)
        self.array_data = []
        self.last_color_info = {}
        self.draw_bars([], {}) # Explicitly draw empty
        self.enable_controls()


    def disable_controls(self):
        self.sort_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.DISABLED)
        self.array_entry.config(state=tk.DISABLED)
        self.algo_menu.config(state=tk.DISABLED)
        self.speed_scale.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

    def enable_controls(self):
        self.sort_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.NORMAL)
        self.array_entry.config(state=tk.NORMAL)
        self.algo_menu.config(state=tk.NORMAL)
        self.speed_scale.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)


# --- Main Execution ---
if __name__ == '__main__':
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()