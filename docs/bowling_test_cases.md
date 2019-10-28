## 测试用例设计

### BowlingTotalPointsTest
* "9- 9- 9- 9- 9- 9- 9- 9- 9- 9-"      # initial    normal 90
* "9- x 9- 9- 9- 9- 9- 9- 9- 9-"      # initial    100
* ”x x x x x x x x x xxx“             # initial    strike 300
* “5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/5”                spare 150

* '9- 9- 9- 9- 9- 9- 9- 9- 9- 9/x'    # Added     100
* ”9- x 3/ 5- 5- 5- 5- 5- 5- xxx“     # Added     104

### FrameFactoryTest
* FrameFactory.create_frame
    * "9- 9- 9- 9- 9- 9- 9- 9- 9- 9-"     # initial   normal       90
    * "9- x 9- 9- 9- 9- 9- 9- 9- 9-"      # initial   has "strike" 100
* 完成SpareFrame, LastFrame后添加测试：
    * ”9- x 3/ 5- 5- 5- 5- 5- 5- xxx“     # Added 104

### SingleFramePointsTest
> frames = FrameFactory.create_frames()

* "9- x 9- 9- 9- 9- 9- 9- 9- 9-"      # initial
    * frames[0].get_points() == 9
    * frames[1].get_points() == 19
    * frames[0].next == frames[1]

* ”9- x 3/ 5- 5- 5- 5- 5- 5- xxx“     # Added  完成SpareFrame/LastFrame后添加
    * frames[2].get_points() == 15
    * frames[9].get_points() == 30
    * not frames[2].has_three_rolls()
    * frames[9].has_three_rolls()

* "9- 9- 9- 9- 9- 9- 9- 9- 9/ 9/x"      # Added 完成SpareFrame和LastFrame后添加
    * frames[0].get_points() == 9
    * frames[8].get_points() == 19
    * frames[9].get_points() == 20
    * not frames[8].has_three_rolls()
    * frames[9].has_three_rolls()

### RollPinsTest
* Frame('9-'):                      # Inital
    * frame.get_first_roll_pins(),
    * frame.get_total_rolls_pins(),

* Frame('35')                       # Inital 8
* StrikeFrame('x')      # Inital
* SpareFrame('9/')      # Added
* LastFrame('9/x')      # Added
* LastFrame('9/5')      # Added
* LastFrame('xxx')      # Added

### BowlingSequenceExceptionTest

