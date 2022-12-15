import {Box, Card, CardContent, Typography} from "@mui/material";
import React, { useContext } from "react";
import StrategiesCard from "./StrategiesCard";
import { StrategiesContext } from "../../../StrategiesContext";

function Strategies({ toggle, strategy }) {
  const { strategies } = useContext(StrategiesContext);
  
  const filteredStrategies = strategies && strategies.filter((item) => {
    return item.isProduction === true
  })
  
  return (
    <>
        {filteredStrategies ? <Box
            component="main"
            sx={{
                ml: 1,
                p: 1,
                display: "flex",
                flexWrap: "wrap",
            }}>
            {filteredStrategies.map((data, i) => {
                return (
                    <StrategiesCard
                        props={data}
                        key={i}
                        toggle={toggle}
                        strategy={strategy}
                    />
                );
            })}
        </Box>:
            <Box sx={{display: "flex", justifyContent:"center", alignItems:"center", height:"90vh"}}>
              <Card
                  sx={{
                    width: "500px",
                    ml: 4,
                    boxShadow: "0px 0px 10px 5px rgba(0,0,0,0.1)",
                    transition: " all .15s ease-in-out",
                    borderRadius: 3,
                    backgroundColor: "red",
                    color: "white",
                  }}>
                <CardContent>
                  <Typography
                      variant="h1"
                      sx={{ fontSize: "3rem", fontWeight: 600, m: 1 }}>
                    Error!
                  </Typography>
                  <Typography
                      variant="p"
                      sx={{ fontWeight: 400, m: 1 }}>
                    An unknown error has occurred while loading the contents of this page. Please logout and try again later.
                    We are sorry for the inconvenience caused.
                  </Typography>
                </CardContent>
              </Card>
        </Box>
        }

    </>
  );
}

export default Strategies;
