from configuration import ELEVATOR_CAPACITY, ELEVATOR_LOAD_TIME

class Elevator():
  def __init__(self):
    self.capacity = ELEVATOR_CAPACITY
    self.current_floor = 0
    self.target_floors = []
    self.direction = 0 # Options: -1 = Down, 0 = Idle, 1 = Up
    self.passangers = []
    self.wait_time = 0

  # Process actions (if any) for this tick
  def act(self, going_up, going_down):

    # Wait (Doors, opening/closing, etc.)
    if self.wait_time > 0:
      self.wait_time -= 1

    # No orders currently
    elif len(self.target_floors) == 0:
      self.direction = 0

    # Stop on a floor to drop people
    elif self.current_floor == self.target_floors[0]:
      # Add wait time
      self.wait_time = ELEVATOR_LOAD_TIME

      # Remove floor from targets
      self.target_floors.pop()

      # Let people out
      for passanger in self.passangers:
        if passanger.target_floor == self.current_floor:
          passanger.exit_elevator()

      # Get people in
      new_passangers = going_up if self.direction > 0 else going_down
      # Add to passangers
      self.passangers += new_passangers

      for new_passanger in new_passangers:
        # Inform people they have entered the elevator
        new_passanger.enter_elevator()
        # Add new target floors
        self.go_to_floor(new_passanger.target_floor)

    # Move a floor
    elif self.current_floor != self.target_floors[0]:
      self.current_floor += self.direction

    # Error case
    else:
      print("Elevator confused")

  def go_to_floor(self, floor):
    # Add to targets
    self.target_floors.append(floor)

    # Remove duplicates
    self.target_floors = list(set(self.target_floors))

    # Compute new direction if idle
    self.direction = 1 if self.target_floors[0] > self.current_floor else -1

    # Reorder targets
    self.target_floors.sort()
    # Reverse if going down
    if self.direction < 0:
      self.target_floors.reverse()

  # Reset for a new day
  def reset(self):
    self.current_floor = 0
    self.passangers = []
