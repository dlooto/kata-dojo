## 本训练中的题目

### Get Environment
```
git@github.com:dlooto/training.git
mkvirtualenv pyall    # pyall is your <virtualenv_name>
workon pyall

cd training
pip install -U -r requirements.txt
```

### Run Tests
```
workon pyall   # the python3.6 virtualenv
cd training/tests
pytest -v unit/test_gildedrose.py 

```


[Gilded Rose](docs/gildedrose.md)


[All Kata](http://codingdojo.org/kata/)
