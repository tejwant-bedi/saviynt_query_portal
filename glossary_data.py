glossary_data = {
        "REQUEST_ACCESS (TYPE)": {
            "ADD": 1,
            "UPDATEAC": 12,
            "REMOVE": 2,
            "UPDATEROLE": 3,
            "REMOVEROLE": 4,
            "PROPOSEDACCOUNTOWNERS": 15,
            "MODIFY_ORGANIZATION": 16,
            "PROPOSEDENTOWNERS": 17,
            "CREATEUSER": 18,
            "UPDATEUSER": 19,
            "CREATERULE": 20,
            "UPDATERULE": 21,
            "DISABLERULE": 22,
            "MODIFYPRIVILEGE": 23,
            "FFID": 24,
            "FFIDACCESS": 25,
            "T2PUPLOAD": 26
        },

        "REQUEST_ACCESS (STATUS)": {
            "DEFAULT": 1,
            "APPROVED": 2,
            "TASKCREATED": 3,
            "REJECTED": 4,
            "COMPLETED": 5,
            "AFTERENDDATEREVOKETASKCREATED": 6,
            "TASKDURATIONEXPIRED": 7,
            "DISCONTINUE": 6
        },

        "ACCESS_APPROVERS (STATUS)": {
            "ASSIGNED_BUT_NO_SHOW": -1,
            "NEW": 1,
            "APPROVED": 2,
            "REJECTED": 3,
            "ESCLATE": 4,
            "EXPIRE": 5,
            "DISCONTINUE": 6,
            "REASSIGNED": 7
        },

        "ACCESS_APPROVERS (SERIALTYPE)": {
            "SEND_TO_ALL_AND_APPROVE_BY_ONE": 1,
            "SEND_TO_ALL_AND_APPROVE_BY_ALL": 2,
            "SEND_TO_ALL_SERIAL": 3,
            "REQUIREDENTITLEMENT_INREQUEST": -1,
            "NON_REQUIREDENTITLEMENT_INREQUEST": -6
        },
        
        "ACCESS_APPROVERS (APPROVERTYPE)": {
            "USER": 1,
            "USER_GROUP": 2
        },
        
        "ARSREQUESTS (REQUEST TYPE)": {
            "ADD": 1,
            "UPDATEACCOUNT": 12,
            "DEL": 2,
            "NEWACCOUNT": 3,
            "NEWROLEREQUEST": 4,
            "CREATEROLE": 5,
            "MODIFYROLE": 6,
            "CREATE_BADGE": 7,
            "REPLACE_BADGE": 8,
            "UPDATE_BADGE": 9,
            "REMOVE_BADGE": 10,
            "NEWFFROLEREQUEST": 11,
            "PROPOSEDACCOUNTOWNERS": 15,
            "MODIFY_ORGANIZATION": 16,
            "PROPOSEDENTOWNERS": 17,
            "CREATEUSER": 18,
            "UPDATEUSER": 19,
            "CREATERULE": 20,
            "UPDATERULE": 21,
            "DISABLERULE": 22,
            "FIREFIGHTERID": 23,
            "FIREFIGHTERIDACCESS": 24,
            "T2P": 25,
            "ENABLERULE": 26,
            "EXTENDACCESS": 28,
            "ENABLEACCOUNT": 29,
            "DISABLEACCOUNT": 30,
            "LOCKACCOUNT": 31,
            "UNLOCKACCOUNT": 32
        },
        
        "ARS_REQUESTS (STATUS)": {
            "STATUS_DRAFT": 0,
            "STATUS_INPROCESS": 2,
            "STATUS_NEW": 1,
            "STATUS_EXPIRES": 4,
            "STATUS_COMPLETED": 3,
            "STATUS_DISCONTINUE": 6,
            "STATUS_ARCHIVE": 7
        },
        
        "ARSTASKS (STATUS)": {
            "STATUS_NEW": 1,
            "STATUS_INPROGRESS": 2,
            "STATUS_COMPLETE": 3,
            "STATUS_DISCONTINUE": 4,
            "STATUS_PENDINGCREATE": 5,
            "STATUS_PENDINGPROV": 6,
            "STATUS_PROVFAILED": 7,
            "STATUS_ERROR": 8,
            "STATUS_NO_ACTION_REQUIRED": 9
        },    
        
        "ARSTASKS (OWNERTYPE)": {
            "OWNERTYPE_USER": 1,
            "OWNERTYPE_USER_GROUP": 2
        },    
        
        "ARSTASKS (TASKTYPE)": {
            "ADD": 1,
            "DEL": 2,
            "NEWACCOUNT": 3,
            "NEWROLEREQUEST": 4,
            "CHANGEPASSWORD": 5,
            "ENABLEACCOUNT": 6,
            "PROPOSEDACCOUNTOWNERS": 7,
            "DELETEACCOUNT": 8,
            "UPDATEUSER": 9,
            "UPDATEACCOUNT": 12,
            "PROPOSEDENTOWNERS": 13,
            "DISABLEACCOUNT": 14,
            "MODIFYPRIVILEGE": 23,
            "CREATEENTITLEMENT": 24,
            "UPDATEENTITLEMENTACCESSADD": 25,
            "UPDATEENTITLEMENTACCESSREMOVE": 26,
            "UPDATEENTITLEMENT": 27,
            "DELETEENTITLEMENT": 28,
            "FIREFIGHTERIDGRANTACCESS": 29,
            "FIREFIGHTERIDREVOKEACCESS": 30,
            "EXTENDACCESS": 31,
            "LOCKACCOUNT": 32,
            "UNLOCKACCOUNT": 33,
            "FIREFIGHTERINSTANCE_GRANTACCESS": 34,
            "FIREFIGHTERINSTANCE_REVOKEACCESS": 35
        },       
        
        "ARSTASKS (SOURCE)": {
            "REQUEST": "REQUEST",
            "CERTIFICATION": "CERTIFICATION",
            "ZERODAY": "ZERODAY",
            "PROVRULE": "PROVRULE",
            "SOD": "SOD",
            "ONECLICKDISABLE": "ONECLICKDISABLE",
            "ANALYTICS": "ANALYTICS",
            "ROLES": "ROLES",
            "FFID_GRANT": "FFID_GRANT",
            "FFID_REVOKE": "FFID_REVOKE",
            "PAM_BOOTSTRAP": "PAM_BOOTSTRAP",
            "UPDATE_ROLE": "UPDATE_ROLE",
            "FFINSTANCE_GRANT": "FFINSTANCE_GRANT",
            "FFINSTANCE_REVOKE": "FFINSTANCE_REVOKE",
            "PRECEDENCE": "PRECEDENCE",
            "DEESCALATION": "DEESCALATION",
            "WEBSERVICE": "WEBSERVICE"
        }, 
        
        "ENTITLEMENT VALUES (STATUS)": {
            "ACTIVE": 1,
            "INACTIVE": 2,
            "DECOMMISSION_ACTIVE": 3,
            "DECOMMISSION_INACTIVE": 4,
            "STATUS_DELETED": 5
        },     
                
        "ENTITLEMENT VALUES (SYS CRITICAL)": {
            "NONE": 0,
            "VERYLOW": 1,
            "LOW": 2,
            "MEDIUM": 3,
            "HIGH": 4,
            "VERYHIGH": 5
        },  
        
        "ENTITLEMENT VALUES (SOX CRITICAL)": {
            "NONE": 0,
            "VERYLOW": 1,
            "LOW": 2,
            "MEDIUM": 3,
            "HIGH": 4,
            "VERYHIGH": 5
        },    
        
        "ENTITLEMENT VALUES (RISK)": {
            "NONE": 0,
            "VERYLOW": 1,
            "LOW": 2,
            "MEDIUM": 3,
            "HIGH": 4,
            "VERYHIGH": 5
        },       
        
        "ENTITLEMENT VALUES (ENT CRITICAL)": {
            "ACTIVE": 1,
            "INACTIVE": 2,
            "PROCESSING": 6
        },    
        
        "CAMPAIGN (STATUS)": {
            "COMPLETED": 2,
            "DISCONTINUED": 6,
            "EXPIRED": 7,
            "INPROGRESS": 5,
            "LAUNCHING": 8,
            "NEW": 1,
            "PREVIEW": 4
        },       
        
        "CAMPAIGN (TYPE)": {
            "APPLICATIONOWNER_METADATA": 9,
            "APPLICATION_OWNER": 8,
            "ENTITLEMENTOWNER": 1,
            "ORGANIZATION": 7,
            "ROLEOWNER": 5,
            "SELF_CERTIFICATION": 3,
            "SERVICEACCOUNT": 6,
            "USERMANAGER": 2
        },           
       
        "CERTIFICATION (TYPE)": {
            "APPLICATIONOWNER_METADATA": 9,
            "APPLICATION_OWNER": 8,
            "ENTITLEMENT_OWNER": 1,
            "ORGANIZATION": 7,
            "ROLE_OWNER": 5,
            "SELF_CERTIFICATION": 3,
            "SERVICE_ACCOUNT": 6,
            "USER_MANAGER": 2
        },      
            
        "CERTIFICATION (STATUS)": {
            "BASEDON_CERTIFIER": 3,
            "DISCONTINUED": 5,
            "STATUSCOMPLETED": 2,
            "STATUSEXPIRED": 4,
            "STATUSLOCKED": 3,
            "STATUSLOCKEDANDTASKCREATED": 8,
            "STATUS_CANCELLED": 9,
            "STATUS_DISCONTINUED": 7,
            "STATUS_FULLY_EXECUTED": 10,
            "STATUS_INPROGRESS": 1,
            "STATUS_NEW": 0,
            "STATUS_PREVIEW": 6
        },      
        
        "ANALYTICSCONFIGES (ANALYTICSTYPE)": {
            "ESQUERY": 8,
            "MANUAL": 6,
            "PRECONFIG": 1,
            "RUNTIME": 5,
            "RUNTIMEPREVENTATIVE": 7,
            "SQL": 2
        },          
        
        "ANALYTICSCONFIGES (SECURITY CONTEXT)": {
            "SECURITY_CONTEXT_NONE": 0,
            "SECURITY_CONTEXT_ORGANIZATION": 2,
            "SECURITY_CONTEXT_USER": 1
        },   
        
        "ATTESTATIONS (TYPE)": {
            "BASEDON_CERTIFIER": 3,
            "BASEDON_ROLEKEYS": 1,
            "BASEDON_ROLEQUERY": 2,
            "DISCONTINUED": 5,
            "STATUSCOMPLETED": 2,
            "STATUSLOCKED": 3,
            "STATUS_NEW": 0,
            "STATUS_INPROGRESS": 1,
            "STATUSEXPIRED": 4,
            "TYPE_CRITICAL_ACCESS": 4,
            "TYPE_ENTOWNER": 1,
            "TYPE_FF": 3,
            "TYPE_ROLEOWNER": 5,
            "TYPE_SERVICE_ACCOUNT": 6,
            "TYPE_USER_MANAGER": 2
        },       
        
        "CUSTOMER (STATUS)": {
            "STATUS_ACTIVE": 1,
            "STATUS_INACTIVE": 0
        },      
        
        "CUSTOMER (TYPE)": {
            "DATA_SECURITY": 1,
            "GROUPING": 2,
            "REQUEST_RULES": 3
        },      
        
        "EMAILHISTORY (STATUS)": {
            "SENDNOW": 1,
            "SENT": 2,
            "JBPMSEND": 4,
            "ERRORWHILESEND": 404,
            "PROCESSED": 14,
            "GRANTPROCESSED": 17,
            "PROCESSEDADDED": 144,
            "GRANTPROCESSEDADDED": 177
        },    
        
        "EXTERNALCONNECTIONS (STATUS)": {
            "SUCCESSFUL": 1,
            "FAILED": 0,
            "ENABLE": 1,
            "DISABLE": 0
        },         
        
        "HANARULE (OWNER)": {
            "USER": 1,
            "USERGROUP": 2
        },

        "HANARULE (STATUS)": {
            "ACTIVE": 0,
            "INACTIVE": 1
        },

        "HANARULE (TYPE)": {
            "BUISNESS": 0,
            "TECH": 1,
            "USERUPDATE": 2,
            "NEWUSER": 3,
            "REMOVEUSER": 4,
            "UPDATE_ENTITLEMENT": 5,
            "NEW_ENTITLEMENT": 6,
            "REMOVE_ENTITLEMENT": 7,
            "REQUEST": 8
        },

        "HANARULE (EVENTSOURCE)": {
            "EVENT_SOURCE_NEWUSER_VIA_UI": 1,
            "EVENT_SOURCE_NEWUSER_VIA_IMPORT": 2,
            "EVENT_SOURCE_NEWUSER_VIA_API": 3,
            "EVENT_SOURCE_UPDATEUSER_VIA_UI": 4,
            "EVENT_SOURCE_UPDATEUSER_VIA_IMPORT": 5,
            "EVENT_SOURCE_UPDATEUSER_VIA_API": 6,
            "EVENT_SOURCE_REMOVEUSER_VIA_UI": 7
        },         
        
        "ROLES (STATUS)": {
            "INACTIVE": 0,
            "ACTIVE": 1,
            "COMPOSING": 2,
            "SENTFORAPPROVAL": 3,
            "DECOMMISION": 4,
            "MINING": 5
        },   
        
        "ROLES (TYPE)": {
            "NONE": 0,
            "ENABLER": 1,
            "TRANSACTIONAL": 2,
            "FIREFIGHTER": 3,
            "ENTERPRISE": 4,
            "APPLICATION": 5,
            "ENTITLEMENTBASEDROLE": 6
        }                      
    }