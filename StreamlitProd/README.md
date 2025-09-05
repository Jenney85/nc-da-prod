
# jm-nc-dashboard

Streamlit app for Nature Counter Health Outcome and Journal reporting.

## pages
- 📊 Health Outcome Reports
- 📓 Journal Reports
- Seamspace Emotion Reports (Pending; excluded from current version)

## How to Run
streamlit run NC-Generic-Loin-v1.py
Only authorized users can access based on permissions.csv.


## Notes

- More notes to be added

Prefered structure should look like this:
Main –
Dashboard (branch/project)
Master # Master will call different sub = HO , Journal, and Seamspace, but they should all be under folder “Pages”
| generic login
| permission.cvs
| readme
| ignore
- are we supposed to have data source in Master? Can it be in folder, called “Source”
- === here are the data source at this time ==
| HO data (HealthOutcome Data)
| Journal data
| Seamspace data
pages
- === These are the HO codes ===
| HO 1.py
| HO 2.py
- can “| HO data” reside here?? Or should it be in “Master”
- === These are the Journal codes ===
| Journal 1.py
- can | Journal data reside here?? Or should it be in “Master”
- === T These are the Seamspace (my client) codes ===
| Seamspace 1.py
- can | Seamspace data reside here?? Or should it be in “Master”

Intake (as separate project/branch)
| intake login
| permission.cvs
| readme
| ignore
pages
|Intake-view-update.py
|Intake-data

Prefered structure should look like this: <br>
Main – <br>
      Dashboard (branch/project) <br>
      Master    # Master will call different sub = HO , Journal, and Seamspace, but they should all be under folder “Pages” <br>
        | generic login <br>
        | permission.cvs <br>
        | readme <br>
        | ignore <br>
        # are we supposed to have data source in Master? Can it be in folder, called “Source” <br>
        # === here are the data source at this time == <br>
         | HO data  (HealthOutcome Data) <br>
         | Journal data <br>
         | Seamspace data <br>
        Pages <br>
             # === These are the HO codes === <br>
            | HO 1.py <br>
            | HO 2.py  <br>
            # can “| HO data” reside here?? Or should it be in “Master” <br>
            # === These are the Journal codes === <br>
            | Journal 1.py <br>
            # can | Journal data reside here?? Or should it be in “Master” <br>
            # === T These are the Seamspace (my client) codes === <br>
            | Seamspace 1.py <br>
           # can | Seamspace data reside here?? Or should it be in “Master” <br> \

   Intake (as separate project/branch) <br>
        | intake login  <br>
        | permission.cvs <br>
        | readme <br>
        | ignore <br>
         Pages <br>
             |Intake-view-update.py <br>
             |Intake-data <br>

>>>>>>> 08985fbb44ea5f2aa393ecccfdb8b44f971449cc


