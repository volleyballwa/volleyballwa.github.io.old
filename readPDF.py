import pandas as pd
import definitions


def master(venues, league, date, token):
    head = 'https://vwa.bracketpal.com/dailyform/'
    fixtures = list()
    for i in league:
        print(head)
        print(i)
        print(date)
        url = head + str(i) + "/" + str(date)
        print(url)
        table_MN = pd.read_html(url)
        try:
            df = table_MN[2]
            for index, row in df.iterrows():
                if row[0] != "Time" and type(row[1]) != type(0.01):
                    venue = row[1].split(" Ct")[0].replace(" Ct", "")
                    if venue in venues:
                        court = row[1].split("Ct")[1]
                        team_a = row[2]
                        team_b = row[5]
                        try:
                            duty = row[7][5:]
                        except TypeError:
                            duty = " "
                        division = definitions.div_dict[url.split('/')[-2]][1]
                        _date = url.split('/')[-1].split('-')
                        date_dd = _date[2]
                        date_mm = _date[1]
                        date_yyyy = _date[0]
                        time = row[0].split(':')
                        time_hr = time[0].zfill(2)
                        time_min = time[1]

                        tmp_venue = definitions.venues_dict[venue.lower()].split("*")
                        venue_0 = tmp_venue[0]
                        venue_1 = tmp_venue[1]
                        venue_2 = tmp_venue[2]

                        fixture = definitions.Fixture(venue, venue_0, venue_1, venue_2, court, team_a, team_b, duty,
                                                      division, date_dd, date_mm, date_yyyy, time_hr, time_min)
                        fixtures.append(fixture)
        except IndexError:
            pass

    files = []

    for i in fixtures:
        file_out = definitions.APP_ROOT + "\\WAVL Scoresheets\\temp\\" + token + "\\" + i.venue + "-" + i.court + "-" + i.time_hr + i.time_min + ".pdf"
        canvas_data = definitions.get_overlay_canvas(i)
        form = definitions.merge(canvas_data, template_path=definitions.pdf_default)
        definitions.save(form, filename=file_out)
        files.append(file_out)

    output = definitions.APP_ROOT + "\\WAVL Scoresheets\\output\\" + token + ".pdf"
    files.sort()
    definitions.merge_pdfs(files, output)