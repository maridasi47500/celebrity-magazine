
mkdir templates 
python3 scaffold.py language name short_name
python3 scaffold.py country name
python3 scaffold.py place name
python3 scaffold.py stage name
python3 scaffold.py user username email password country_id:references language_id:references
python3 scaffold.py chatmode language_id:references content user_id:references did_you_mean
python3 scaffold.py post place_id:references language_id:references content user_id:references did_you_mean
python3 scaffold.py fakepost stage_id:references language_id:references content user_id:references did_you_mean
