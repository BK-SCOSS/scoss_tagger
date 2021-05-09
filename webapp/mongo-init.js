db.createUser(
  {
                user: "scoss_admin",
                pwd: "scoss_admin",
    roles: [
      {
                            role: "readWrite",
                            db: "scoss"
                        
      }
                  
    ]
            
  }
  
);

db = db.getSiblingDB('scoss')
