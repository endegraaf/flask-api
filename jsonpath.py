import json
import jsonpath_ng

#json_data = {'foo': [{'baz': 1}, {'baz': 2}]}
json_data = {
  "Data": [
    {
      "List": [
        {
          "requestid": 52537,
          "jobrolename": "Tester/Testautomatiseerder",
          "locationname": "Apeldoorn",
          "availability": "35",
          "maximumpurchaseprice": 'null',
          "maximumpurchasepricesortable": "0.00",
          "prolongation": True,
          "publishdate": "2021-10-14T15:04:57Z",
          "finalreactiondate": "2021-10-21T21:59:00Z",
          "rolelevelname": "Senior",
          "enddate": "2021-12-30T23:00:00Z",
          "startdate": "2021-11-14T23:00:00Z",
          "brokerpartyid": 17604,
          "brokerpartyname": "Between",
          "requesterpartyid": 59884,
          "requesterpartyname": "Belastingdienst  ICT (2018)",
          "readablereference": "2021/6100-2021-IBS-6334",
          "teaser": "Voor onze eindklant Belastingdienst zoeken wij een Tester/Testautomatiseerder.",
          "customerlogourl": "https://jobcatcherdata.blob.core.windows.net/jobcatcher-public/production/images/59884/59884"
        },
        {
          "requestid": 52841,
          "jobrolename": "Test automation engineer",
          "locationname": "Odijk/Thuis",
          "availability": "40,00",
          "maximumpurchaseprice": 'null',
          "maximumpurchasepricesortable": "0.00",
          "prolongation": True,
          "publishdate": "2021-10-28T08:00:21Z",
          "finalreactiondate": "2021-11-04T11:00:00Z",
          "rolelevelname": "Professional",
          "enddate": "2023-01-31T23:00:00Z",
          "startdate": "2022-01-31T23:00:00Z",
          "brokerpartyid": 30888,
          "brokerpartyname": "Yellow Friday",
          "requesterpartyid": 31681,
          "requesterpartyname": "Sogeti",
          "readablereference": "2021/6393-20211027-T",
          "teaser": "Yellow Friday zoekt een Test automation engineer.",
          "customerlogourl": "https://jobcatcherdata.blob.core.windows.net/jobcatcher-public/production/images/31681/31681"
        }
      ],
      "AllowedActions": [],
      "Amount": 28
    }
  ],
  "Errors": [],
  "ResultCode": "SUCCESS"
}

jsonpath_expr = jsonpath_ng.parse('$.Data.[0].List.[0].requestid')
list_val = [match.value for match in jsonpath_expr.find(json_data)]

print(list_val)