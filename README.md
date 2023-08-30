# Use Case Summary

## Project Context:
This project aims to cluster a private bank's clients based on their behavior. This case requires to develop a customer segmentation to define marketing strategy to insure customer's satisfaction. 

![image](https://blog.kakaocdn.net/dn/QEkfG/btqwVfT2p4u/lCWHbDjHHOaFxjqpT2ASOK/img.png)

## Dataset overview:
The dataset has about 834754 customers along with 44 features for each to help determine their behaviour towards the bank. 
The table represents some of the important variables needed for the segmentation:

 | Variables  | Description  | DType |
| :------------ |:---------------:| -----:|
| CLIENT_AGE      | The client's age  |Numeric |
| CLIENT_MMM      | The client's Average Monthly Flow (Salary)        |   Numeric |
| CLIENT_VRD_MOY | The client's average actual value of deposits        |   Numeric |
| CLIENT_PROFESSION | The client's profession        |   Categorical |
| PACK |The client's enrolement to the offered packs (TRUE , FALSE)       |   Categorical |
| CLIENT_TYPE_DEPOSANT | The client's  deposit type ( savings , tansactions..)       |   Categorical |
| CLIENT_ENTREE_FINAL | The client's seniority (CONQUETE, AUTRES)        |   Categorical |
| CLIENT_ENROLES | The client's enrolement to the bank's remote services (TRUE, FALSE)       |   Categorical |
| CLIENT_NOMBRE_CARTES | The client's cards number        |   Numeric |
| TOTAL_PACK | The client's average actual value of deposits        |   Numeric |
| CLIENT_VRD_MOY | The client's total packs number        |   Numeric |

## Methodology :
### Crisp-DM

Cross-industry standard process for data mining, known as CRISP-DM, is an open standard process model that describes common approaches used by data mining experts. It is the most widely-used analytics model.

![image](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/CRISP-DM_Process_Diagram.png/479px-CRISP-DM_Process_Diagram.png)

### Objectives :

- Business understanding
- Data Understanding
- Data Preparation
- Modeling
- Evaluation
- Deployment

## Challenges :
- Very large dataset
- Extremely skewed data



