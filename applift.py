
# ['BidId', 'TrafficType', 'PublisherId', 'AppSiteId', 'AppSiteCategory', 'Position', 'BidFloor',
#  'Timestamp', 'Age', 'Gender', 'OS', 'OSVersion', 'Model', 'Manufacturer', 'Carrier', 'DeviceType',
#  'DeviceId', 'DeviceIP', 'Country', 'Latitude', 'Longitude', 'Zipcode', 'GeoType', 'CampaignId', 'CreativeId',
#  'CreativeType', 'CreativeCategory', 'ExchangeBid', 'Outcome']


import graphlab as gl


# train=gl.SFrame('applift_train_final.csv')
# test=gl.SFrame('applift_test_final.csv')

train=gl.SFrame('applift_train_datas.csv')
test=gl.SFrame('applift_train_datas.csv')


train['Outcome']=train['Outcome'].astype(float)

trainBasic=gl.SFrame({'user_id':train['DeviceIP'],'item_id':train['CreativeId'],'Outcome':train['Outcome']})
trainUser=gl.SFrame({'user_id':train['DeviceIP'],'TrafficType':train['TrafficType'],'PublisherId':train['PublisherId'],'AppSiteId':train['AppSiteId'],'AppSiteCategory':train['AppSiteCategory'],'Position':train['Position'],'BidFloor':train['BidFloor'],'Age':train[ 'Age'],'Gender':train['Gender'],'OS':train[ 'OS'],'OSVersion':train['OSVersion'],'Model':train[ 'Model'],'Manufacturer':train['Manufacturer'],'Carrier':train[ 'Carrier'],'DeviceType':train['DeviceType'],'Country':train[ 'Country'],'GeoType':train['GeoType']})
trainProduct=gl.SFrame({'item_id':train['CreativeId'],'CreativeType':train['CreativeType'],'CreativeCategory':train['CreativeCategory']})

model1= gl.factorization_recommender.create(trainBasic, target='Outcome',
                                                user_data=trainUser,
                                               item_data=trainProduct,num_factors=70,side_data_factorization=True,max_iterations=50,random_seed=50)

testBasic=gl.SFrame({'user_id':test['DeviceIP'],'item_id':test['CreativeId']})
testUser=gl.SFrame({'user_id':test['DeviceIP'],'TrafficType':test['TrafficType'],'PublisherId':test['PublisherId'],'AppSiteId':test['AppSiteId'],'AppSiteCategory':test['AppSiteCategory'],'Position':test['Position'],'BidFloor':test['BidFloor'],'Age':test[ 'Age'],'Gender':test['Gender'],'OS':test[ 'OS'],'OSVersion':test['OSVersion'],'Model':test[ 'Model'],'Manufacturer':test['Manufacturer'],'Carrier':test[ 'Carrier'],'DeviceType':test['DeviceType'],'Country':test[ 'Country'],'GeoType':test['GeoType']})
testProduct=gl.SFrame({'item_id':test['CreativeId'],'CreativeType':test['CreativeType'],'CreativeCategory':test['CreativeCategory']})


predictions=model1.predict(testBasic, new_user_data=testUser,new_item_data=testProduct)


Outoutcome=gl.SArray(predictions)
Outuser_ID=gl.SArray(test['DeviceIP'])
Outcreative_ID=gl.SArray(test['CreativeId'])
Actoutcome = gl.SArray(test['Outcome'])
Testexchbid = gl.SArray(test['ExchangeBid'])


Submission=gl.SFrame({'User_ID':Outuser_ID,'Creative_ID':Outcreative_ID,'ActualOutcome':Actoutcome,'PredOutcome':Outoutcome,'Excbid':Testexchbid})


Submission.save('appliftoutfact',format='csv')


import  pandas as pd

df = pd.read_csv('appliftoutfact.csv')

result = df.sort(['PredOutcome'],ascending = [0])

result.to_csv('pandasoutput_small.csv',index=False)

# result.to_csv('pandasoutput_full.csv',index=False)










