import React, { useState } from "react";
import {Tabs, Tab, Box} from "@mui/material"
import HandleOptions from "./HandleOptions";
const TabPanel = (props) => {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`tabpanel-${index}`}
            {...other}
        >
            {value === index && (
                <Box>
                   {children}
                </Box>
            )}
        </div>
    );
}

const OptionRoot = () => {
    const [value, setValue] = useState(0);
    const nifty = ["api/get_nifty/", "api/get_nifty_histo/", ["NIFTY SPOT", "NIFTY FUT", "INDIA VIX"],50];
    const banknifty = ["api/get_banknifty/", "api/get_banknifty_histo/", ["BANKNIFTY SPOT", "BANKNIFTY FUT", "INDIA VIX"],100];


    return (
        <Box>
            <Tabs value={value} onChange={(event,value) => setValue(value)} aria-label="basic tabs example">
                <Tab label="NIFTY" />
                <Tab label="BANKNIFTY" />
            </Tabs>

            <TabPanel value={value} index={0}>
                <HandleOptions option={nifty}/>
            </TabPanel>
            <TabPanel value={value} index={1}>
                <HandleOptions option={banknifty}/>
            </TabPanel>
        </Box>
    )
}

export default OptionRoot;