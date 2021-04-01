import { useState, useEffect, useRef } from 'react';
import { useHistory } from "react-router-dom";

//uses the react-router history's state as a temporary storage for state.
//This is useful for restoring form state when returning to a page and you
//  don't want to store the values in the url, in localStorage, or a redux store
//see: Scene, MemeEditor
/* eslint-disable react-hooks/exhaustive-deps */
export function useHistoryState(key, initValue) {
    const history = useHistory();

    const [value, setValue] = useState(() => {
        let historyValue = null;
        try {
            historyValue = history.location.state ? history.location.state[key] : null;
        } catch(error) {}

        //console.log('key: ', key, 'historyValue', historyValue);
        if(historyValue !== null && historyValue !== undefined) {
            return historyValue;
        } else {
            return initValue;
        }
    })
    useEffect(() => {
        let nstate = history.location.state ? { ...history.location.state} : {};
        nstate[key] = value;
        history.replace(history.location.pathname, nstate);
        //console.log('key: ',key, 'value', value, 'state', history.location.state)
    }, [key, value])
    return [value, setValue];
}
/* eslint-enable react-hooks/exhaustive-deps */

export function usePrevious(value) {
    const ref = useRef();
    useEffect(() => {
        ref.current = value;
    });
    return ref.current;
}
