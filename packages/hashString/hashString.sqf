params ["_string",""];
_parameters = format["./scripts/scriptHash.py & scriptHash & %1",_string]; //Format the arguments 
_result = "armaxpy" callExtension _parameters;

/*
As the result is an hex string,bad characters could've been created
during the sending process of data through the socket,let's clean the string
*/


private _allowedChars= ("abcdefghijklmnopqrstuvwxyz" splitString "") + ("1234567890" splitString "");
private _strArray = _result splitString "";
private _toRemove = [];
{
    
    if not(_x in _allowedChars) then {
        _toRemove pushBack _forEachIndex;
    };
    
} forEach _strArray; //Let's fetch which characters should get removed

reverse _toRemove;

{
    _strArray deleteAt _x;
    
} count _toRemove;  

_finalString = _strArray joinString "";

_finalString; //Our cleaned string hash